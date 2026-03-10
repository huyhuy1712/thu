from __future__ import annotations

import os

# Disable Xet storage backend — its DLL is blocked by Windows Application Control
# policies on some machines, causing huggingface_hub to crash at model download time.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import argparse
import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from deep_translator import GoogleTranslator
from faster_whisper import WhisperModel
from imageio_ffmpeg import get_ffmpeg_exe
from yt_dlp import YoutubeDL


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Download a public video/audio URL, transcribe it with timestamps, '
            'translate each segment, and export JSON/SRT outputs.'
        )
    )
    parser.add_argument('source', help='Public video/audio URL or local file path.')
    parser.add_argument(
        '--output-dir',
        default='output/transcripts',
        help='Directory where output files will be written.',
    )
    parser.add_argument(
        '--output-name',
        default='',
        help='Optional base filename for output files.',
    )
    parser.add_argument(
        '--model',
        default='small',
        help='faster-whisper model size, for example tiny, base, small, medium, large-v3.',
    )
    parser.add_argument(
        '--source-lang',
        default='auto',
        help='ASR source language code. Use auto for detection.',
    )
    parser.add_argument(
        '--target-lang',
        default='vi',
        help='Translation target language code, for example vi or en.',
    )
    parser.add_argument(
        '--device',
        default='cpu',
        help='Inference device for faster-whisper: cpu, cuda.',
    )
    parser.add_argument(
        '--compute-type',
        default='int8',
        help='Compute type for faster-whisper, for example int8, float16, float32.',
    )
    parser.add_argument(
        '--beam-size',
        type=int,
        default=1,
        help='Beam size used by faster-whisper.',
    )
    parser.add_argument(
        '--merge-gap-seconds',
        type=float,
        default=0.8,
        help='Merge neighboring speech segments when silence gap is smaller than this value.',
    )
    parser.add_argument(
        '--max-event-seconds',
        type=float,
        default=14.0,
        help='Upper bound duration for one merged speech event.',
    )
    parser.add_argument(
        '--vad-filter',
        action='store_true',
        help='Enable VAD filter. Keep disabled for music-heavy videos to avoid missing lyrics.',
    )
    parser.add_argument(
        '--no-translation',
        action='store_true',
        help='Skip segment translation and export source transcript only.',
    )
    parser.add_argument(
        '--bilingual-srt',
        action='store_true',
        help='Include original and translated text in SRT output.',
    )
    parser.add_argument(
        '--long-only',
        action='store_true',
        help='Export only one continuous script text file without segmented outputs.',
    )
    parser.add_argument(
        '--translate-workers',
        type=int,
        default=10,
        metavar='N',
        help='Number of parallel threads for translation (default: 10). Increase for faster translation, but too high may trigger rate-limiting.',
    )
    parser.add_argument(
        '--translate-chunk-chars',
        type=int,
        default=3000,
        metavar='N',
        help='Character size for long-only translation chunks (default: 3000).',
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Fast mode: use tiny model + beam size 1 for quicker results (lower quality).',
    )
    return parser.parse_args()


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)


def slugify_filename(value: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9._-]+', '-', value.strip())
    cleaned = cleaned.strip('-._')
    return cleaned[:120] or 'transcript'


def ensure_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_or_resolve_source(source: str, temp_dir: Path) -> tuple[Path, str]:
    if not is_url(source):
        local_path = Path(source).expanduser().resolve()
        if not local_path.exists():
            raise FileNotFoundError(f'Source file not found: {local_path}')
        return local_path, local_path.stem

    ffmpeg_dir = str(Path(get_ffmpeg_exe()).parent)
    ydl_opts: dict[str, Any] = {
        'format': 'bestaudio/best',
        'outtmpl': str(temp_dir / '%(title).120s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': ffmpeg_dir,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=True)
        prepared = Path(ydl.prepare_filename(info))
        requested_downloads = info.get('requested_downloads') or []
        if requested_downloads:
            filepath = requested_downloads[0].get('filepath')
            if filepath:
                prepared = Path(filepath)
        title = info.get('title') or prepared.stem

    if not prepared.exists():
        raise FileNotFoundError('Unable to locate downloaded media file.')

    return prepared, title


def extract_audio_to_wav(source_path: Path, temp_dir: Path) -> Path:
    ffmpeg_executable = get_ffmpeg_exe()
    output_audio = temp_dir / 'audio_16k_mono.wav'
    command = [
        ffmpeg_executable,
        '-y',
        '-i',
        str(source_path),
        '-vn',
        '-acodec',
        'pcm_s16le',
        '-ar',
        '16000',
        '-ac',
        '1',
        str(output_audio),
    ]
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode != 0:
        stderr_text = (result.stderr or b'').decode('utf-8', errors='replace').strip()
        raise RuntimeError(stderr_text or 'ffmpeg failed to extract audio.')
    return output_audio


def format_timestamp(seconds: float, for_srt: bool = False) -> str:
    total_milliseconds = max(int(round(seconds * 1000)), 0)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1000)
    separator = ',' if for_srt else '.'
    return f'{hours:02}:{minutes:02}:{secs:02}{separator}{milliseconds:03}'


def safe_translate(translator: GoogleTranslator, text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ''
    try:
        translated = translator.translate(stripped)
    except Exception:
        return stripped
    return translated.strip() if translated else stripped


def translate_segments_parallel(
    segments: list[dict[str, Any]],
    target_lang: str,
    max_workers: int = 10,
) -> None:
    """Translate all segments in parallel, writing results back in-place."""
    # GoogleTranslator is not thread-safe to share, so create one per worker call.
    def _translate_one(idx: int, text: str) -> tuple[int, str]:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return idx, safe_translate(translator, text)

    total = len(segments)
    print(f'[translate] Dịch {total} đoạn song song (max_workers={max_workers})...')
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_translate_one, i, seg['text']): i
            for i, seg in enumerate(segments)
        }
        done = 0
        for future in as_completed(futures):
            idx, translated = future.result()
            segments[idx]['translated_text'] = translated
            done += 1
            if done % 20 == 0 or done == total:
                print(f'[translate] {done}/{total} đoạn đã dịch xong')


def split_text_to_chunks(text: str, chunk_chars: int) -> list[str]:
    clean = re.sub(r'\s+', ' ', text).strip()
    if not clean:
        return []

    size = max(int(chunk_chars), 500)
    words = clean.split(' ')
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for word in words:
        addition = len(word) if not current else len(word) + 1
        if current and current_len + addition > size:
            chunks.append(' '.join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += addition

    if current:
        chunks.append(' '.join(current))
    return chunks


def translate_long_script_parallel(
    segments: list[dict[str, Any]],
    target_lang: str,
    chunk_chars: int,
    max_workers: int,
) -> str:
    source_script = ' '.join(seg.get('text', '').strip() for seg in segments if seg.get('text', '').strip())
    chunks = split_text_to_chunks(source_script, chunk_chars)
    if not chunks:
        return ''

    def _translate_chunk(idx: int, text: str) -> tuple[int, str]:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return idx, safe_translate(translator, text)

    print(
        f'[translate] Dịch long-only theo {len(chunks)} chunk song song '
        f'(chunk_chars={max(int(chunk_chars), 500)}, max_workers={max_workers})...'
    )

    results: list[str] = [''] * len(chunks)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_translate_chunk, i, chunk): i
            for i, chunk in enumerate(chunks)
        }
        done = 0
        for future in as_completed(futures):
            idx, translated = future.result()
            results[idx] = translated
            done += 1
            if done % 5 == 0 or done == len(chunks):
                print(f'[translate] chunk {done}/{len(chunks)} xong')

    return ' '.join(part.strip() for part in results if part.strip())


def transcribe_audio(
    audio_path: Path,
    model_size: str,
    source_lang: str,
    device: str,
    compute_type: str,
    beam_size: int,
    vad_filter: bool,
    merge_gap_seconds: float,
    max_event_seconds: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    language = None if source_lang == 'auto' else source_lang
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    raw_segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=beam_size,
        vad_filter=vad_filter,
        condition_on_previous_text=True,
    )

    rows: list[dict[str, Any]] = []
    for index, segment in enumerate(raw_segments, start=1):
        text = segment.text.strip()
        if not text:
            continue
        start = float(segment.start)
        end = float(segment.end)
        rows.append(
            {
                'id': index,
                'start': round(start, 3),
                'end': round(end, 3),
                'start_ts': format_timestamp(start),
                'end_ts': format_timestamp(end),
                'text': text,
            }
        )

    rows = merge_speech_events(rows, merge_gap_seconds, max_event_seconds)

    metadata = {
        'language': getattr(info, 'language', source_lang),
        'language_probability': getattr(info, 'language_probability', None),
        'duration': getattr(info, 'duration', None),
    }
    return rows, metadata


def merge_speech_events(
    rows: list[dict[str, Any]],
    merge_gap_seconds: float,
    max_event_seconds: float,
) -> list[dict[str, Any]]:
    if not rows:
        return rows

    merged: list[dict[str, Any]] = [rows[0].copy()]
    merge_gap_seconds = max(merge_gap_seconds, 0.0)
    max_event_seconds = max(max_event_seconds, 1.0)

    for row in rows[1:]:
        current = merged[-1]
        gap = float(row['start']) - float(current['end'])
        merged_duration = float(row['end']) - float(current['start'])
        should_merge = (
            gap <= merge_gap_seconds
            and merged_duration <= max_event_seconds
            and not str(current['text']).rstrip().endswith(('.', '!', '?'))
        )

        if should_merge:
            current['end'] = row['end']
            current['end_ts'] = row['end_ts']
            current['text'] = f"{current['text']} {row['text']}".strip()
        else:
            merged.append(row.copy())

    for idx, row in enumerate(merged, start=1):
        row['id'] = idx

    return merged


def write_json(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def write_srt(output_path: Path, segments: list[dict[str, Any]], bilingual: bool) -> None:
    lines: list[str] = []
    for segment in segments:
        lines.append(str(segment['id']))
        lines.append(
            f"{format_timestamp(segment['start'], for_srt=True)} --> {format_timestamp(segment['end'], for_srt=True)}"
        )

        translated_text = segment.get('translated_text', '').strip()
        original_text = segment['text'].strip()

        if bilingual and translated_text and translated_text != original_text:
            lines.append(original_text)
            lines.append(translated_text)
        else:
            lines.append(translated_text or original_text)

        lines.append('')

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def write_long_script(output_path: Path, segments: list[dict[str, Any]]) -> None:
    # Build a long readable script by joining translated segment texts.
    merged: list[str] = []
    for segment in segments:
        translated_text = segment.get('translated_text', '').strip()
        original_text = segment.get('text', '').strip()
        text = translated_text or original_text
        if text:
            merged.append(text)

    long_script = ' '.join(merged)
    output_path.write_text(long_script + '\n', encoding='utf-8')


def main() -> int:
    args = parse_args()
    if args.fast:
        args.model = 'tiny'
        args.beam_size = 1

    output_dir = ensure_output_dir(args.output_dir)

    with tempfile.TemporaryDirectory(prefix='video-transcript-') as temp_path:
        temp_dir = Path(temp_path)
        source_path, title = download_or_resolve_source(args.source, temp_dir)
        audio_path = extract_audio_to_wav(source_path, temp_dir)
        segments, metadata = transcribe_audio(
            audio_path=audio_path,
            model_size=args.model,
            source_lang=args.source_lang,
            device=args.device,
            compute_type=args.compute_type,
            beam_size=args.beam_size,
            vad_filter=args.vad_filter,
            merge_gap_seconds=args.merge_gap_seconds,
            max_event_seconds=args.max_event_seconds,
        )

    target_lang = '' if args.no_translation else args.target_lang.strip().lower()
    long_script_override = ''
    if target_lang:
        if args.long_only:
            long_script_override = translate_long_script_parallel(
                segments=segments,
                target_lang=target_lang,
                chunk_chars=args.translate_chunk_chars,
                max_workers=args.translate_workers,
            )
        else:
            translate_segments_parallel(segments, target_lang, max_workers=args.translate_workers)
    else:
        for segment in segments:
            segment['translated_text'] = segment['text']

    output_name = slugify_filename(args.output_name or title)
    json_path = output_dir / f'{output_name}.json'
    srt_path = output_dir / f'{output_name}.srt'
    script_path = output_dir / f'{output_name}.script.txt'

    payload = {
        'source': args.source,
        'title': title,
        'model': args.model,
        'source_language': metadata['language'],
        'source_language_probability': metadata['language_probability'],
        'target_language': None if args.no_translation else target_lang,
        'segment_count': len(segments),
        'segments': segments,
    }

    if long_script_override:
        script_path.write_text(long_script_override + '\n', encoding='utf-8')
    else:
        write_long_script(script_path, segments)

    if not args.long_only:
        write_json(json_path, payload)
        write_srt(srt_path, segments, bilingual=args.bilingual_srt)
        print(f'JSON output: {json_path}')
        print(f'SRT output: {srt_path}')

    print(f'Script output: {script_path}')
    print(f'Segments: {len(segments)}')
    print(f"Detected language: {metadata['language']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())