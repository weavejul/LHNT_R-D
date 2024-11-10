from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: str):
        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message to {connection.client}: {e}")
                to_remove.append(connection)
        for connection in to_remove:
            self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive by receiving (and ignoring) messages from the client
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def send_periodic_data():
    while True:
        # Example data
        vector = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # Replace with your dynamic data
        text = "Hello, Quest 3!"  # Replace with your dynamic text

        message = {
            "vector": vector,
            "text": text
        }

        # Serialize the message to JSON
        message_json = json.dumps(message)

        # Broadcast the message to all connected clients
        await manager.broadcast(message_json)

        # Wait for 0.1 seconds (10 times per second)
        await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_periodic_data())
