### AI SERVICE

Quickstart

1. Create a virtual environment (recommended) and install deps:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# or cmd.exe
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app with serve:

```bash
serve run app.main:deployment --reload
```

3. Check service ready:  

Go to `localhost:8000` to see the welcome message, done!


### API Endpoints

#### Sign Language Recognition
```bash
POST /v3/api/sign-language/recognize
```

#### Request

| Name           | Type   | Required | Description                               |
|----------------|--------|----------|-------------------------------------------|
| platform       | string | Yes      | Client platform (e.g. `web`, `mobile`)    |
| language_code  | string | Yes      | Language code (e.g. `au`, `vn`)            |

#### Body Json

```json
{
  "frames": ["keypoints_frame_1", "keypoints_frame_2",...],
  "previous_word": ""
}
```

#### Response

```json
{
    "data": [{
    "class": "hello",
    "confidence": 0.92
     }]
}
```