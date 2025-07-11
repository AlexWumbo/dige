from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import wave
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    with wave.open(tmp_path, 'rb') as audio:
        frame_rate = audio.getframerate()
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        n_frames = audio.getnframes()
        duration_sec = n_frames / frame_rate
        bitrate_kbps = frame_rate * channels * sample_width * 8 / 1000

    return {
        "duration_seconds": round(duration_sec, 2),
        "frame_rate": frame_rate,
        "channels": channels,
        "bitrate_kbps": round(bitrate_kbps, 2),
        "note": "This version skips clipping detection"
    }
