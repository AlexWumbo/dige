from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import tempfile, os

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

    audio = AudioSegment.from_file(tmp_path)
    samples = audio.get_array_of_samples()
    max_val = max(samples)
    min_val = min(samples)
    clipping = max_val >= audio.max_possible_amplitude or min_val <= -audio.max_possible_amplitude

    duration_sec = len(audio) / 1000
    frame_rate = audio.frame_rate
    channels = audio.channels
    bitrate_kbps = audio.frame_rate * audio.sample_width * audio.channels / 1000 * 8

    os.unlink(tmp_path)

    return {
        "duration_seconds": duration_sec,
        "frame_rate": frame_rate,
        "channels": channels,
        "bitrate_kbps": bitrate_kbps,
        "clipping_detected": clipping
    }
