from fastapi import FastAPI, WebSocket
from STT_local import transcribe_audio_bytes
from hf_llm import ask_hf
from tts_eleven import text_to_speech

app = FastAPI()

@app.websocket("/ws/audio")
async def audio_ws(ws: WebSocket):
    await ws.accept()
    print("🔗 WebSocket client connected")

    try:
        while True:
            data = await ws.receive_bytes()
            print(f"🎤 Received {len(data)} bytes of audio")

            user_text = await transcribe_audio_bytes(data)
            print(f"🗣️ Transcribed text: {user_text}")

            assistant_text = await ask_hf(user_text)
            print(f"🤖 Assistant reply: {assistant_text}")

            audio_path = await text_to_speech(assistant_text)
            print(f"🔊 TTS saved to: {audio_path}")

            await ws.send_json({
                "user_text": user_text,
                "assistant_text": assistant_text,
                "audio_path": audio_path
            })

    except Exception as e:
        print("❌ WebSocket closed:", e)
