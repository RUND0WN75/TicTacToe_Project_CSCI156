import socket
import time

class Server:
  def __init__(self):
    self.host = "localhost"
    self.port = 8080
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((self.host, self.port))
    self.server.listen(10)
    self.client, self.address = self.server.accept()
    self.gameOver = False
    self.turn = "X"
    self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    self.you = "X"
    self.opponent = "O"
    self.computer = "O"
  
  def displayBoard(self):
    