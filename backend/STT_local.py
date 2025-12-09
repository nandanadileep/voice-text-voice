from faster_whisper import WhisperModel
import io
import tempfile
import soundfile as sf
import numpy as np
import asyncio
from typing import Optional, Union, List, Dict

# Load once at startup
model = WhisperModel("small", device="cpu", compute_type="int8")


async def transcribe_audio_bytes(
    audio_bytes: bytes,
    language: Optional[str] = None,
    vad_filter: bool = True,
    return_timestamps: bool = False  
) -> Union[str, List[Dict]]:

    if not audio_bytes:
        return "[empty audio]"

    loop = asyncio.get_running_loop()

    try:
        return await loop.run_in_executor(
            None,
            _sync_transcribe,
            audio_bytes,
            language,
            vad_filter,
            return_timestamps
        )

    except Exception as e:
        print("❌ Transcription failed:", str(e))
        return "[error]"


def _sync_transcribe(audio_bytes, language, vad_filter, return_timestamps):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        data, samplerate = sf.read(io.BytesIO(audio_bytes), dtype="float32")

        # Stereo → Mono
        if data.ndim > 1:
            data = np.mean(data, axis=1)

        sf.write(tmp.name, data, samplerate)

        segments, info = model.transcribe(
            tmp.name,
            language=language,
            vad_filter=vad_filter,
            beam_size=5,
            best_of=5,
        )

        if return_timestamps:
            output = []
            for seg in segments:
                output.append({
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip()
                })
            return output

        # Default: plain text
        text_parts = [seg.text.strip() for seg in segments if seg.text.strip()]
        final_text = " ".join(text_parts)

        return final_text if final_text else "[no speech detected]"
