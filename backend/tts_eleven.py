import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
client = ElevenLabs(api_key=ELEVEN_API_KEY)

async def text_to_speech(text: str, output_path="reply.wav") -> str:
    """
    Generate speech from text using Eleven Labs and save to a WAV file.
    Returns the file path.
    """
    try:
        # Correct method: client.text_to_speech.convert()
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice ID
            model_id="eleven_turbo_v2",
            output_format="mp3_44100_128"  # or "pcm_16000" for WAV
        )
        
        # Collect the audio bytes from the generator
        audio_bytes = b"".join(audio_generator)
        
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
