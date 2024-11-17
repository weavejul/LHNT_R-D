# server.py
# local PC command: uvicorn server:app --host 0.0.0.0 --port 8000
# local network command: ws://10.150.52.215:8000/ws
# see apis running local command: ps aux | grep uvicorn  

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    Initializes the ConnectionManager and starts the periodic data sender.
    """
    print("Application startup")
    
    # Initialize the ConnectionManager and store it in app state for accessibility
    manager = ConnectionManager()
    app.state.manager = manager
    
    # Start the background task to send periodic data
    data_sender = asyncio.create_task(send_data(manager))
    
    try:
        yield
    finally:
        # Cancel the background task gracefully on shutdown
        data_sender.cancel()
        print("Application shutdown")

app = FastAPI(lifespan=lifespan)

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasting messages to connected clients.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a WebSocket connection and adds it to the active connections list.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: str):
        """
        Sends a message to all connected WebSocket clients.
        Removes clients that encounter errors during message sending.
        """
        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message to {connection.client}: {e}")
                to_remove.append(connection)
        for connection in to_remove:
            self.disconnect(connection)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that manages client connections and keeps them alive.
    Receives and ignores incoming messages to maintain the connection.
    """
    manager: ConnectionManager = app.state.manager
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive by receiving (and ignoring) messages from the client
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def send_data(manager: ConnectionManager):
    """
    Sends data to clients
    """
    while True:
        # Example data - replace with your dynamic data as needed
        vector = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] #replace with output of CapsNet
        text = "Message Sent"  # Example text data
        # Create the message payload
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