import socket
import threading

class Peer:
  def __init__ (self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connections = []
    
  def connect(self, peer_host, peer_port):
    try:
      connection = self.socket.connect((peer_host, peer_port))
      self.connections.append(connection)
      print("Connected to peer at " + peer_host + ":" + str(peer_port))
    except socket.error as e:
      print(f"Failed to connect to peer at {peer_host}:{peer_port}. Error: {e}")
      
  def listen(self):
    self.socket.bind((self.host, self.port))
    self.socket.listen(5)
    print(f"Listening for connections on {self.host}:{self.port}")
    
    while True:
      conn, addr = self.socket.accept()
      self.connections.append(conn)
      print(f"Accepted connection from {addr}")
      
  def broadcast(self, message):
    for conn in self.connections:
      try:
        conn.sendall(message.encode())
      except socket.error as e:
        print(f"Failed to send message to peer. Error: {e}")
        
  def start(self):
    listen_thread = threading.Thread(target=self.listen)
    listen_thread.start()
    