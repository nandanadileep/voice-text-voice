from fastapi import FastAPI, WebSocket
from STT_local import transcribe_audio_bytes

app = FastAPI()

@app.get("/health")
def health():
    return("Status: ok")

@app.websocket("/ws/audio")
async def audio_ws(ws: WebSocket):
    await ws.accept()
    print("🔗 WebSocket client connected")

    try:
        while True:
            data = await ws.receive_bytes()
            print(f"🎤 Received {len(data)} bytes of audio")
            text = await transcribe_audio_bytes(data)
            print(f"🗣️ Transcribed text: {text}")
            await ws.send_json({"text": text})
    except Exception as e:
        print("❌ WebSocket closed:", e)
