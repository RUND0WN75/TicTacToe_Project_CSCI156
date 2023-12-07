import socket
import threading
import random

class TicTacToe:
  def __init__(self):
    self.board = [[0 for col in range(3)] for row in range(3)]
    self.players = ["X", "O"]
    self.turn = self.players[0]
    self.player1 = "Player 1"
    self.player2 = "Player 2"
    self.winner = None
    self.gamePlay = None
    self.gameOver = False
    
    self.counter = 0
    
  def computerMove(self):
    move = [random.randint(0, 2), random.randint(0, 2)]
    while not self.isValidMove(move):
      move = [random.randint(0, 2), random.randint(0, 2)]
    return move
    
  def makeMove(self, move, player=None):
    if self.gameOver:
      return
    
    if player == None:
      player = self.turn
      
    self.counter += 1
    self.board[int(move[0])][int(move[1])] = player
    
    if self.checkWinner():
      if self.winner == self.players[0]:
        if self.gamePlay == "computer":
          print("You win!")
        elif self.gamePlay == "human":
          print(f"{self.player1} wins!")
        else:
          print(f"{self.player1} wins!")
      elif self.winner == self.players[1]:
        if self.gamePlay == "computer":
          print("You lose!")
        elif self.gamePlay == "human":
          print(f"{self.player2} wins!")
        else:
          print(f"{self.player2} wins!")

      self.gameOver = True
    else:
      if self.counter == 9:
        print("Its a tie!")
        self.gameOver = True
    
  def isValidMove(self, move):
    return self.board[int(move[0])][int(move[1])] == 0
  
  def checkWinner(self):
    for row in range(3):
      if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
        self.winner = self.board[row][0]
        self.gameOver = True
        return True
    
    for col in range(3):
      if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
        self.winner = self.board[0][col]
        self.gameOver = True
        return True
    
    if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
      self.winner = self.board[0][0]
      self.gameOver = True
      return True
    elif self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
      self.winner = self.board[0][2]
      self.gameOver = True
      return True
    
    return False
  

class Server:
  def __init__(self, ip_address="localhost", port=3333):
    self.ip_address = ip_address
    self.port = 3333
    self.server = None
    self.clients = []
    self.p2pHosts = [] #[(handle, (ip, port)), ...]
    self.activeP2PGames = [] #[(handle, handle), ...]
    self.activeGames = {} #{handle: TicTacToe, ...}
    
  def handleClient(self, client_socket, client_address):
    try:
      message = f"connected::{str(client_address)}"
      self.sendMessage(client_socket, message)
      
      while True:
        request = self.receiveMessages(client_socket, client_address)
        print(f"[Message Received] Client: {client_address[0]}:{client_address[1]}")
        
        if request == False:
          self.sendMessage(client_socket, "invalid")
          continue
        elif request == None:
          client_socket.send("closed".encode("utf-8"))
          break
        else:
          pass
        
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        clientHandle = self.getClientByAddr(client_address)[2]
        self.clients.remove((client_socket, client_address, clientHandle))
        client_socket.close()
        print(f"Connection to client ({client_address[0]}:{client_address[1]}) closed")
    
  def handleTaken(self, handle):
    for client in self.clients:
      if client[2] == handle:
        return True
    return False
  
  def getClientByHandle(self, handle):
    for client in self.clients:
      if client[2] == handle:
        return client
    return None
  
  def getClientByAddr(self, addr):
    for client in self.clients:
      if client[1] == addr:
        return client
    return None
  
  def getActiveGameByHost(self, handle):
    for game in self.activeP2PGames:
      if game[0] == handle:
        return game
    return None
  
  def getP2PHostByHandle(self, handle):
    for host in self.p2pHosts:
      if host[0] == handle:
        return host
    return None
  
  def receiveMessages(self, client_socket, client_address):
    client_request = client_socket.recv(1024).decode("utf-8")
    lead = client_request.split("::")[0]
    
    match lead.lower():
      case "ping":
        clientHandle = self.getClientByAddr(client_address)[2]
        self.activeGames[clientHandle] = TicTacToe()
        activeGame = self.activeGames[clientHandle]
        activeGame.gamePlay = "computer"
        
        self.sendMessage(client_socket, "pong")
        return True
      
      case "move":
        move = eval(client_request.split("::")[1])
        clientHandle = self.getClientByAddr(client_address)[2]
        activeGame = self.activeGames[clientHandle]
        activeGame.makeMove(move, activeGame.players[0])
        
        computerMove = activeGame.computerMove()
        activeGame.makeMove(computerMove, activeGame.players[0])
        self.sendMessage(client_socket, f"move::{str(computerMove)}")
          
        return True
      
      case "game_over":
        clientHandle = self.getClientByAddr(client_address)[2]
        activeGame = self.activeGames[clientHandle]
        activeGame.gameOver = True
        self.activeGames.pop(clientHandle)
        return True
      
      case "handle":
        handle = client_request.split("::")[1]
        if self.handleTaken(handle):
          self.sendMessage(client_socket, "invalid")
          return None
        
        self.clients.append((client_socket, client_address, handle))
        self.sendMessage(client_socket, "accepted")
        return True
      
      case "connect":
        hostReq = eval(client_request.split("::")[1])
        hostClient = self.getClientByHandle(hostReq[0])
        hostSocket = hostClient[0]
        connClient = self.getClientByAddr(client_address)
        
        player1 = hostClient[2]
        player2 = connClient[2]
        self.p2pHosts.remove(hostReq)
        self.activeP2PGames.append((player1, player2))
        
        self.sendMessage(hostSocket, "player_connected")
        
        return True
        
      case "host_active":
        hostHandle = self.getClientByAddr(client_address)[2]
        activeGame = self.getActiveGameByHost(hostHandle)
        
        if activeGame:
          connClient = self.getClientByHandle(activeGame[1])
          clientSocket = connClient[0]
          self.sendMessage(clientSocket, "player_connected")
          return True
        else:
          return False
      
      case "host":
        port = client_request.split("::")[1]
        if (len(self.p2pHosts) > 0):
          handle = self.getClientByAddr(client_address)[2]
          matching_host = self.getP2PHostByHandle(handle)
          if not matching_host:
            self.p2pHosts.append((handle, (client_address[0], port)))
        else:
          handle = self.getClientByAddr(client_address)[2]
          self.p2pHosts.append((handle, (client_address[0], port)))
          
        return True
      
      case "hosts":
        if len(self.p2pHosts) > 0:
          self.sendMessage(client_socket, f"hosts::{str(self.p2pHosts)}")
          return True
        else:
          self.sendMessage(client_socket, f"hosts::{str([])}")
          return True
      
      case "close":
        conn_client = self.getClientByAddr(client_address)
        if conn_client:
          self.clients.remove(conn_client)
          return None
        else:
          return False
      case _:
        return False
      
  def sendMessage(self, client_socket, msg):
    client_socket.send(msg.encode("utf-8"))
    
  def run(self):
    try:
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.server.bind((self.ip_address, self.port))
      self.server.listen()
      print("The server for CSCI 156 Project Group 4 has started")
      
      while True:
        try:
          client_socket, client_address = self.server.accept()
          print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
          thread = threading.Thread(target=self.handleClient, args=(client_socket, client_address,))
          thread.start()
        except KeyboardInterrupt:
          print("Keyboard Interrupt")
          break
      
    except Exception as e:
        print(f"Error: {e}")
    finally:
        self.server.close()
        
if __name__ == "__main__":
  server = Server("10.0.0.24")
  server.run()