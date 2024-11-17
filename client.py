# test_client.py
# local PC command: uvicorn server:app --host 0.0.0.0 --port 8000
# local network command: ws://10.150.52.215:8000/ws
# see apis running local command: ps aux | grep uvicorn

import asyncio
import websockets
import json
average_array = [0,0,0,0,0,0]
count_array = [0,0,0,0,0,0]
#processes vector (add running average functionality)
def find_max_index(arr):
    """
    Updates the average_array to store cumulative running averages across calls.

    Parameters:
    - arr: Current input array to process.
    - average_array: External array to maintain cumulative averages.
    - count_array: External array to track the number of updates at each index.

    Returns:
    - max_index: Index of the maximum value greater than 1/6 in the array, or -1 if none.
    """
    vector_range = 1 / 6
    if len(arr) == 0:
        return None  # Return None if the array is empty
    
    if len(average_array) != len(arr) or len(count_array) != len(arr):
        raise ValueError("average_array and count_array must be the same size as arr")
    
    max_index = -1
    max_value = arr[0]
    
    # Update averages and find the max index
    for i in range(len(arr)):
        # Update cumulative average
        count_array[i] += 1
        average_array[i] = ((average_array[i] * (count_array[i] - 1)) + arr[i]) / count_array[i]
        
        # Check for max value above threshold
        if arr[i] > max_value and arr[i] > vector_range:
            max_value = arr[i]
            max_index = i
    print(average_array)        
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