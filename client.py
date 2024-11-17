# test_client.py
# local PC command: uvicorn server:app --host 0.0.0.0 --port 8000
# local network command: ws://10.150.52.215:8000/ws
# see apis running local command: ps aux | grep uvicorn

import asyncio
import websockets
import json

#processes vector (add running average functionality)
def find_max_index(arr):
    vector_range = 1/6
    if len(arr) == 0:
        return None  # Return None if the array is empty
    
    max_index = -1  # Start with -1 in max_index (if nothing above 1/6 resting)
    max_value = arr[0]
    
    # Loop through the array to find the maximum value and its index
    for i in range(1, len(arr)):
        if arr[i] > max_value and arr[i] > vector_range:
            max_value = arr[i]
            max_index = i
            
    return max_index

async def listen():
    uri = "ws://10.148.2.38:8000/ws"  # Use 'localhost' if running on the same machine
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                index = find_max_index(data.get("vector", []))
                text = data.get("text", "")
                print(f"Received Vector: {index}")
                print(f"Received Text: {text}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(listen())