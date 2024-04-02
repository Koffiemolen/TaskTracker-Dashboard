# backend/app/websocket_manager.py
""" This module contains the ConnectionManager class which
    is responsible for managing the WebSocket connections.
"""
from asyncio import Lock
from fastapi import WebSocket


class ConnectionManager:
    """Class to manage WebSocket connections."""

    def __init__(self):
        # Dictionary where keys are group names and values are lists of WebSocket connections
        self.active_connections = {}
        self.lock = Lock()

    async def connect(self, websocket: WebSocket, channel: str = "default"):
        """Connect a WebSocket and assign it to a channel."""
        async with self.lock:
            if channel not in self.active_connections:
                print(f"channel {channel} not in active connections, assigning to it")
                self.active_connections[channel] = []
            else:
                print(f"channel {channel} is in active connections, appending it")
            self.active_connections[channel].append(websocket)
            await websocket.accept()

    async def disconnect(self, websocket: WebSocket, channel: str = "default"):
        """Disconnect a WebSocket from a channel."""
        async with self.lock:
            print(f"Disconnecting to channel: {channel}")
            if channel in self.active_connections and websocket in self.active_connections[channel]:
                self.active_connections[channel].remove(websocket)
                if not self.active_connections[channel]:
                    del self.active_connections[channel]

    async def broadcast(self, message: str, group: str = "default"):
        """Broadcast a message to all connections in a specified group."""
        async with self.lock:
            print(f"function: broadcast - broadcasting message: {message}")
            print(f"function: broadcast - sending to channel: {group}")
            for channel, connections in self.active_connections.items():
                print(f"function: broadcast - screaming to channel: {channel}")
                if group == "default" or group == channel:  # pylint: disable=no-else-return
                    for connection in connections:
                        try:
                            print(f"function: broadcast - sending message: {connection}")
                            await connection.send_text(message)
                        except Exception as e:  # pylint: disable=broad-except
                            # Consider logging the error and removing the connection if it's closed
                            print(f"function: broadcast - Error sending message: {e}")
                else:
                    print(f"function: broadcast - group: {group} is not default andnot channel")
            print("function: broadcast - Is finished")

manager = ConnectionManager()
