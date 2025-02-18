import whisper
import os
import tempfile
import soundfile as sf
import ffmpeg
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model (change to "tiny", "base", "small", etc.)
model = whisper.load_model("small")

def convert_to_wav(input_path):
    """Convert audio/video file to WAV format for Whisper."""
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    ffmpeg.input(input_path).output(output_path, format="wav").run(overwrite_output=True)
    return output_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads and transcribes."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Convert to WAV if necessary
    if not filepath.endswith(".wav"):
        filepath = convert_to_wav(filepath)

    # Transcribe with Whisper
    result = model.transcribe(filepath)
    return jsonify({"transcription": result["text"]})

@app.route("/record", methods=["POST"])
def record_audio():
    """Receives recorded audio from frontend and transcribes."""
    audio_data = request.files["audio"]
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_data.save(temp_wav.name)

    # Transcribe with Whisper
    result = model.transcribe(temp_wav.name)
    return jsonify({"transcription": result["text"]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3050)  # Change 8080 to any free port

