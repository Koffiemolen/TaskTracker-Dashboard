""" This module contains the ConnectionManager class which
    is responsible for managing the WebSocket connections.
"""
from typing import List
from fastapi import WebSocket


class ConnectionManager:
    """Class to manage WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Connects a WebSocket client."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Disconnects a WebSocket client."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Broadcasts a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
