from faster_whisper import WhisperModel
import io
import tempfile
import soundfile as sf

model = WhisperModel("small", device="cpu")

async def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    """
    Transcribe audio bytes to text using local Whisper model.
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            data, samplerate = sf.read(io.BytesIO(audio_bytes))
            sf.write(tmp.name, data, samplerate)
            segments, _ = model.transcribe(tmp.name)
            text = " ".join([seg.text.strip() for seg in segments])
            return text.strip() or "[no speech detected]"
    except Exception as e:
        print("❌ Error during transcription:", e)
        return "[error]"
