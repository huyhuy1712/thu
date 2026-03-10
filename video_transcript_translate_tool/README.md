# Video Transcript Translate Tool

Tool transcribe + translate video/audio to JSON, SRT, and script text.

Pipeline:
1. Load source (YouTube URL or local media file).
2. Extract audio to mono 16 kHz WAV.
3. Transcribe with `faster-whisper`.
4. Merge nearby speech segments.
5. Translate text (optional).
6. Export outputs.

## Quick Start (Windows, simple)

### 1. Install dependencies

Run from repo root:

```powershell
- pip install -r video_transcript_translate_tool/requirements.txt
```

If your virtual env path is different, replace that python path with yours.

### 2. Run basic command

Run from repo root:


```powershell
cd video_transcript_translate_tool
python manage.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 3. Check output

Default output folder:

`video_transcript_translate_tool/output/transcripts`

Files:
- `*.json`: timestamped segments (source + translated text).
- `*.srt`: subtitle file.
- `*.script.txt`: one long readable script.

## Common Commands

### Long-only script (fast to read)

```powershell
python manage.py "https://www.youtube.com/watch?v=VIDEO_ID" --long-only --merge-gap-seconds 0.8 --max-event-seconds 14
```

### Bilingual SRT

```powershell
python manage.py "https://www.youtube.com/watch?v=VIDEO_ID" --target-lang vi --bilingual-srt
```

### No translation (transcript only)

```powershell
python manage.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-translation
```

### Faster but lower quality

```powershell
python manage.py "https://www.youtube.com/watch?v=VIDEO_ID" --fast
```

### Local video file

```powershell
python manage.py "D:/videos/sample.mp4" --target-lang vi
```

## Recommended Defaults

For most cases:

```powershell
python manage.py "URL_OR_FILE" --model small --merge-gap-seconds 0.8 --max-event-seconds 14 --target-lang vi
```

If machine is weak, try:

```powershell
python manage.py "URL_OR_FILE" --fast
```

## Why `python manage.py` sometimes fails

If you run `python manage.py ...` from repo root, it fails because `manage.py` is inside `video_transcript_translate_tool/`.

Use one of these:
- `python video_transcript_translate_tool/manage.py "URL"` (from repo root)
- `cd video_transcript_translate_tool` then `python manage.py "URL"`

## Full Options (summary)

Important options:
- `--output-dir`: output folder path.
- `--output-name`: custom output base filename.
- `--model`: `tiny|base|small|medium|large-v3`.
- `--source-lang`: source language code or `auto`.
- `--target-lang`: translation target language (default `vi`).
- `--no-translation`: skip translation.
- `--bilingual-srt`: write original + translated text in SRT.
- `--long-only`: only write one long script file.
- `--merge-gap-seconds`: merge nearby segments.
- `--max-event-seconds`: max merged segment duration.
- `--translate-workers`: parallel translation workers.
- `--fast`: shortcut for faster lower-quality mode.

## Notes

- First run can be slow because Whisper model is downloaded.
- URL must be publicly accessible.
- Translation uses Google Translate (`deep-translator`), so internet is required.
- `ffmpeg` is bundled through `imageio-ffmpeg` (no global install needed).