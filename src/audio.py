import tempfile
import ffmpeg
from numpy import ndarray
from torch import Tensor
import whisper
import os
from werkzeug.utils import secure_filename 
from fastapi import UploadFile # Add this import

def convert_to_wav(input_path):
    """Convert audio/video file to WAV format for Whisper."""
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    ffmpeg.input(input_path).output(output_path, format="wav").run(overwrite_output=True)
    return output_path


async def save_audio(audio: UploadFile, temp_wav: bool = False):
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    """Save audio file to disk."""
    if temp_wav:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filepath = temp_file.name
    else:
        filename = secure_filename(audio.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(await audio.read())

    # Convert to WAV if necessary
    if not filepath.endswith(".wav"):
        filepath = convert_to_wav(filepath)

    return filepath

def transcribe_audio(audio: str | ndarray | Tensor):
    # Load Whisper model (change to "tiny", "base", "small", etc.)
    # Size	    Parameters	English-only model	Multilingual model	Required VRAM	Relative speed
    # tiny	    39 M	    tiny.en	            tiny	            ~1 GB	        ~10x
    # base	    74 M	    base.en	            base	            ~1 GB	        ~7x
    # small	    244 M	    small.en	        small	            ~2 GB	        ~4x
    # medium	769 M	    medium.en	        medium	            ~5 GB	        ~2x
    # large	    1550 M	    N/A	                large	            ~10 GB	         1x
    # turbo 	809 M	    N/A	                turbo	            ~6 GB	        ~8x
    model = whisper.load_model("small")
    # Transcribe with Whisper
    result = model.transcribe(audio)
    return {"transcription": result["text"]}