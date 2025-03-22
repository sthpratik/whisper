

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import uvicorn
from audio import save_audio, transcribe_audio


app = FastAPI(title="Whisper Transcription API", description="API for audio transcription using Whisper", version="1.0.0")


templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadaudio")
async def upload_file(file: UploadFile = File(...)):
    """Handles file uploads and transcribes."""
    if not file.filename:
        return JSONResponse(content={"error": "No selected file"}, status_code=400)

    filepath = await save_audio(file)

    # Transcribe with Whisper
    return transcribe_audio(filepath)

# Record audio from frontend and stores temporarily
@app.post("/recordaudio")
async def record_audio(audio: UploadFile = File(...)):
    """Receives recorded audio from frontend and transcribes."""
    filepath = await save_audio(audio, temp_wav=True)
    # Transcribe with Whisper
    return transcribe_audio(filepath)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5050)

