from fastapi import FastAPI, WebSocket
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
    except Exception as e:
        print("❌ WebSocket closed:", e)