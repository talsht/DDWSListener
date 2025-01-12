import asyncio
import json
import uuid
import websockets

from DDKeyCloak import DDKeyCloak


class DDSocketListener():
    def __init__(self,
                  WS_URL:str = "wss://testing-ddnode.dd.wwest.local/socket.io/?token=undefined&EIO=3&transport=websocket",
                  token: str=None,
                  environment: int=1,
                  sector: int=0,
                  clientId: str=str(uuid.uuid4()),
                  role: int=2,
                  password: str="",
                  reload: bool=True):
        self.WS_URL = WS_URL
        self.token = token
        self.environment = environment
        self.sector= sector
        self.clientId = clientId
        self.role = role
        self.password = password
        self.reload = reload
        self.listening = False
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.stop_event = asyncio.Event()

    async def websocket_listener(self):
        REGISTER_PAYLOAD = [
            "Register",
            {
                "Environment": self.environment,
                "Sector": self.sector,
                "ClientId": self.clientId,
                "Role": self.role,
                "Password": self.password,
                "Reload": self.reload
            },
            1,
            0,
            self.token
        ]

        try:
            async with websockets.connect(self.WS_URL) as ws:
                print("Connected to WebSocket server.")

                # Send register payload
                await ws.send(f"42{json.dumps(REGISTER_PAYLOAD)}")
                print("Sent register payload.")

                # Listen for messages
                while self.listening:
                    try:
                        # Wait for a message or stop signal
                        done, pending = await asyncio.wait(
                            [ws.recv(), self.stop_event.wait()],
                            return_when=asyncio.FIRST_COMPLETED
                        )

                        if self.stop_event.is_set():
                            break

                        for task in done:
                            message = task.result()
                            print("Received message:", message)
                            await self.message_queue.put(message)
                    except websockets.exceptions.ConnectionClosedOK:
                        print("WebSocket connection closed gracefully.")
                        break
                    except asyncio.CancelledError:
                        break
        except Exception as e:
            print(f"WebSocket connection error: {e}")
        finally:
            print("WebSocket listener stopped.")

    def start_listening(self):
        if self.listening:
            return {"message": "Already listening"}
        self.listening = True
        self.stop_event.clear()
        asyncio.create_task(self.websocket_listener())
        return {"message": "Started listening to WebSocket messages"}

    def stop_listening(self):
        if not self.listening:
            return {"message": "Not currently listening"}
        self.listening = False
        self.stop_event.set()
        return {"message": "Stopped listening to WebSocket messages"}

    async def clear_queue(self):
        """Clear all messages in the queue."""
        while not self.message_queue.empty():
            await self.message_queue.get()
        return {"message": "Queue has been cleared"}


async def try_now():
    keycloak_client = DDKeyCloak(server_url="https://keycloak.dd.wwest.local",
                                 client_id="testing_ddfe",
                                 realm_name="dd-realm",
                                 verify=False)

    token = keycloak_client.get_user_token(username="ddadmin", password="Ad3110$$Ad3110$$")

    print(token)

    socket_listener = DDSocketListener(token=token,
                                       environment=1,
                                       sector=0,
                                       clientId=str(uuid.uuid4()),
                                       role=2,
                                       password="",
                                       reload=True)

    socket_listener.start_listening()
    await asyncio.sleep(10)  # Allow listener to run for some time
    socket_listener.stop_listening()


if __name__ == "__main__":
    asyncio.run(try_now())
