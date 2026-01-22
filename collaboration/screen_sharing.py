"""
Screen Sharing & Remote Control - Remote assistance
"""
import os
import socket
import threading
import base64
from typing import Dict, Optional, Callable
from PIL import ImageGrab
import io
import json


class ScreenSharing:
    """Screen sharing and remote control system"""
    
    def __init__(self, port: int = 8765):
        self.port = port
        self.clients: Dict[str, socket.socket] = {}
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.sharing = False
    
    def start_server(self) -> Dict:
        """Start screen sharing server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            self.running = True
            
            # Start accepting connections
            thread = threading.Thread(target=self._accept_connections)
            thread.daemon = True
            thread.start()
            
            return {"success": True, "port": self.port}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_sharing(self, client_id: str, fps: int = 10) -> Dict:
        """Start sharing screen with client"""
        if client_id not in self.clients:
            return {"success": False, "error": "Client not connected"}
        
        self.sharing = True
        thread = threading.Thread(target=self._share_loop, args=(client_id, fps))
        thread.daemon = True
        thread.start()
        
        return {"success": True, "client_id": client_id}
    
    def _accept_connections(self):
        """Accept client connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_id = f"{address[0]}:{address[1]}"
                self.clients[client_id] = client_socket
                print(f"Client connected: {client_id}")
            except:
                break
    
    def _share_loop(self, client_id: str, fps: int):
        """Screen sharing loop"""
        import time
        frame_time = 1.0 / fps
        
        while self.sharing and client_id in self.clients:
            try:
                # Capture screen
                screenshot = ImageGrab.grab()
                buffer = io.BytesIO()
                screenshot.save(buffer, format='JPEG', quality=70)
                image_data = base64.b64encode(buffer.getvalue()).decode()
                
                # Send to client
                message = json.dumps({
                    "type": "frame",
                    "data": image_data,
                    "timestamp": time.time()
                })
                
                self.clients[client_id].send(message.encode() + b'\n')
                time.sleep(frame_time)
            except Exception as e:
                print(f"Error sharing screen: {e}")
                break
    
    def send_remote_command(self, client_id: str, command: str, 
                           params: Dict = None) -> Dict:
        """Send remote command to client"""
        if client_id not in self.clients:
            return {"success": False, "error": "Client not connected"}
        
        try:
            message = json.dumps({
                "type": "command",
                "command": command,
                "params": params or {}
            })
            self.clients[client_id].send(message.encode() + b'\n')
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stop_sharing(self):
        """Stop screen sharing"""
        self.sharing = False
    
    def stop_server(self):
        """Stop server"""
        self.running = False
        self.sharing = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.clients.values():
            client.close()
        self.clients.clear()


class RemoteControl:
    """Remote control system"""
    
    def __init__(self):
        self.connected = False
        self.server_address: Optional[tuple] = None
    
    def connect(self, host: str, port: int = 8765) -> Dict:
        """Connect to remote server"""
        try:
            self.server_address = (host, port)
            self.connected = True
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_command(self, command: str, params: Dict = None) -> Dict:
        """Send command to remote server"""
        if not self.connected:
            return {"success": False, "error": "Not connected"}
        
        # In production, would use actual socket connection
        return {"success": True, "command": command, "params": params}
