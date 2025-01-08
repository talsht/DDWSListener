import asyncio
import json
import uuid
from collections import deque
from os import environ
import uvicorn
from fastapi import FastAPI, HTTPException
import websockets
from keycloak import KeycloakOpenID
from starlette.responses import RedirectResponse, HTMLResponse

# Configuration
keycloak_openid = KeycloakOpenID(
    server_url="https://keycloak.dd.wwest.local",
    client_id="testers",
    realm_name="dd-realm",
    client_secret_key="ELSV2QYEFbYbl2yAVq56MDNJnfnmN6tD",
    verify=False  # Avoid this in production
)

# Get token
token = keycloak_openid.token(grant_type="client_credentials")
print("Access Token:", token["access_token"])

# Environment check for production
is_production = environ.get("is_production", "False").lower() == "true"
app = FastAPI(openapi_url="/openapi.json" if not is_production else None)

# WebSocket server URL
WS_URL = "wss://testing-ddnode.dd.wwest.local/socket.io/?token=undefined&EIO=3&transport=websocket"

REGISTER_PAYLOAD = [
    "Register",
    {
        "Environment": 1,
        "Sector": 0,
        "ClientId": str(uuid.uuid4()),
        "Role": 2,
        "Password": "",
        "Reload": True
    },
    1,
    0,
    token["access_token"]
]



# Global variables
message_queue = asyncio.Queue()
last_10_messages = deque(maxlen=10)  # Stores the last 10 messages
listening = False
stop_event = asyncio.Event()


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>WebSocket Listener</title>
        </head>
        <body>
            <h1>WebSocket Listener</h1>
            <button onclick="startListening()">Start Listening</button>
            <button onclick="stopListening()">Stop Listening</button>
            <button onclick="clearQueue()">Clear Queue</button>
            <h2>Last 10 Messages</h2>
            <div id="messages"></div>
            <script>
                async function startListening() {
                    const response = await fetch('/start', { method: 'POST' });
                    if (response.ok) {
                        alert('Listening started!');
                    } else {
                        alert('Error starting listener.');
                    }
                }

                async function stopListening() {
                    const response = await fetch('/stop', { method: 'POST' });
                    if (response.ok) {
                        alert('Listening stopped!');
                    } else {
                        alert('Error stopping listener.');
                    }
                }

                async function clearQueue() {
                    const response = await fetch('/clear-queue', { method: 'POST' });
                    if (response.ok) {
                        alert('Queue cleared!');
                        updateMessages([]);
                    } else {
                        alert('Error clearing queue.');
                    }
                }

                async function fetchMessages() {
                    const response = await fetch('/last-10-messages');
                    const data = await response.json();
                    updateMessages(data.messages);
                }

                function updateMessages(messages) {
                    const messagesDiv = document.getElementById("messages");
                    messagesDiv.innerHTML = messages.map(msg => `<p>${msg}</p>`).join("");
                }

                // Fetch messages every 2 seconds
                setInterval(fetchMessages, 2000);
            </script>
        </body>
    </html>
    """


@app.post("/start")
async def start_listening():
    global listening
    if listening:
        return {"message": "Already listening"}
    listening = True
    stop_event.clear()
    asyncio.create_task(websocket_listener())
    return {"message": "Started listening to WebSocket messages"}


@app.post("/stop")
async def stop_listening():
    global listening
    if not listening:
        return {"message": "Not currently listening"}
    listening = False
    stop_event.set()
    return {"message": "Stopped listening to WebSocket messages"}


@app.post("/clear-queue")
async def clear_queue():
    """Clear all messages in the queue and last 10 messages."""
    global last_10_messages
    while not message_queue.empty():
        await message_queue.get()
    last_10_messages.clear()
    return {"message": "Queue has been cleared"}


@app.get("/last-10-messages")
async def get_last_10_messages():
    """Fetch the last 10 messages."""
    return {"messages": list(last_10_messages)}


async def websocket_listener():
    global listening
    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected to WebSocket server.")

            # Send register payload
            await ws.send(f"42{json.dumps(REGISTER_PAYLOAD)}")
            print("Sent register payload.")

            # Listen for messages
            while listening:
                try:
                    # Wait for a message or stop signal
                    done, pending = await asyncio.wait(
                        [ws.recv(), stop_event.wait()],
                        return_when=asyncio.FIRST_COMPLETED
                    )

                    if stop_event.is_set():
                        break

                    for task in done:
                        message = task.result()
                        print("Received message:", message)
                        await message_queue.put(message)
                        last_10_messages.append(message)
                except websockets.exceptions.ConnectionClosedOK:
                    print("WebSocket connection closed gracefully.")
                    break
                except asyncio.CancelledError:
                    break
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        print("WebSocket listener stopped.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)