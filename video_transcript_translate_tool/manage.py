"""
Entry point shortcut — chạy từ trong thư mục video_transcript_translate_tool:

    python manage.py "URL_HOẶC_FILE" [options]

Ví dụ:
    python manage.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python manage.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --target-lang en
    python manage.py "D:/videos/clip.mp4" --model medium --bilingual-srt
    python manage.py "URL" --no-translation
"""

import sys
from pathlib import Path

# Đảm bảo import được module chính dù chạy từ thư mục nào
sys.path.insert(0, str(Path(__file__).parent))

from video_transcript_translate import main

if __name__ == "__main__":
    raise SystemExit(main())
