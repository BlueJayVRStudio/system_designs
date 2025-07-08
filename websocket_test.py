from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uuid

app = FastAPI()

# Serve the static HTML file
@app.get("/")
def get():
    return FileResponse("index.html")

active_connections = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())
    active_connections[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {client_id}: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        del active_connections[client_id]
        print(f"Client {client_id} disconnected.")
