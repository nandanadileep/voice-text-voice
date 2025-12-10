import os
import asyncio
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
if not ELEVEN_API_KEY:
    raise RuntimeError("❌ ELEVEN_API_KEY not found in environment")

client = ElevenLabs(api_key=ELEVEN_API_KEY)


async def text_to_speech(text: str, output_path="reply.wav") -> str:
    """
    Generate speech from text using Eleven Labs and save to an audio file.
    Returns the file path.
    """
    try:
        if not text.strip():
            raise ValueError("Input text is empty")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Auto-select format based on file extension
        ext = os.path.splitext(output_path)[1].lower()
        if ext == ".wav":
            output_format = "pcm_16000"
        else:
            output_format = "mp3_44100_128"

        # Run blocking SDK call safely inside async
        audio_generator = await asyncio.to_thread(
            client.text_to_speech.convert,
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            model_id="eleven_turbo_v2",
            output_format=output_format
        )

        # Collect audio bytes
        audio_bytes = b"".join(audio_generator)

        if not audio_bytes:
            raise RuntimeError("ElevenLabs returned empty audio stream")

        # Save to file
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        print(f"✅ TTS saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error generating TTS: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return ""
