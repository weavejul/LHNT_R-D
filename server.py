# server.py
# local PC command: uvicorn server:app --host 0.0.0.0 --port 8000
# local network command: ws://10.150.52.215:8000/ws
# see apis running local command: ps aux | grep uvicorn  

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List
import serial


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

async def send_data(manager):
    try:
        ser = serial.Serial(port="COM6", baudrate=115200, timeout=1)
        print(f"Serial connection opened on {ser.port} at {ser.baudrate} baud.")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline()
                decoded_line = line.decode('utf-8').strip()
                try:
                    emg_value = int(decoded_line)
                    if emg_value > 100:
                        emg_data = 1
                    else:
                        emg_data = 0
                except ValueError:
                    emg_data = 0

                print(f"Received EMG data: {emg_value}")
                
                # Send the number as a string (e.g., "0", "1", "532", etc.)
                await manager.broadcast(str(emg_data))
            
            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Error in send_data: {e}")