import asyncio
import websockets
import json

# Modify the user_id as needed for testing
user_id = "4"  # Example user_id, replace with the actual user id you want to test with

async def test_real_time_notification():
    # Replace with your WebSocket URL and user_id
    uri = f"ws://localhost:8000/ws/notifications/{user_id}/"

    try:
        # Connect to the WebSocket server
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")

            # Send a test message (Optional, depends on how your system is set up)
            test_message = {
                "type": "send_notification",
                "message": "Test notification"
            }
            await websocket.send(json.dumps(test_message))

            # Receive notifications in real-time
            while True:
                response = await websocket.recv()
                print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

# Run the test
asyncio.get_event_loop().run_until_complete(test_real_time_notification())
