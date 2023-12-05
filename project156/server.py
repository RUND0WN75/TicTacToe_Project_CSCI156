import socket
import threading
import random
import time
import sys

class Server:
  def __init__(self):
    self.host = "localhost"
    self.port = 3333
    self.server = None
    self.clients = list()
    self.p2pHosts = list()
    
  def startServer(self):
    try:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        print("The server for CSCI 156 Project Group 4 has started")
        self.server.listen(10)
        while True:
          try: 
            self.connectPlayers()
            self.listen()
            
          except KeyboardInterrupt:
            print("\nClosing server...")
            self.server.close()
            print("Server closed.")
            sys.exit()
    except KeyboardInterrupt:
        print("\nClosing server...")
        self.server.close()
        print("Server closed.")
        sys.exit()
    except socket.error as e:
        print("Error", e)
  
  def connectPlayers(self):
    try:
      client, addr = self.server.accept()
      if client and addr:
        print('connect attempt')
        handle = self.getClientMessage([client, addr, None])
      
        self.clients.append((client, addr, handle))
        for client in self.clients:
          print("[CONNECTED] {} - [{}:{}]".format(client[2], str(client[1][0]), str(client[1][1])))
      else:
        self.listen()

      
    except KeyboardInterrupt:
      print("\nClosing server...")
      self.server.close()
      print("Server closed.")
      sys.exit()
    except socket.error as e:
      print("Error", e)
 
  def filterClients(self, client):
    clientList = filter(lambda x: x[0] != client, self.clients)
    return clientList
   
  def getClientMessage(self, client):
    clientConn = client[0]
    if not clientConn:
      return None
    
    data = clientConn.recv(2048)
    if not data:
      clientConn.close()
      return None
    else:
      lead = data.decode("utf-8")
      
      if lead == "handle":
        handle = clientConn.recv(2048).decode("utf-8")
        return handle
    
      if lead == "clients":
        clientList = self.filterClients(client)
        clientStr = str(clientList)
        clientConn.send("clients".encode("utf-8"))
        clientConn.send(clientStr.encode("utf-8"))
        return True
      
      if lead == "hosts":
        hostList = []
        for host in self.p2pHosts:
          hostList.append((str(host[0]), str(host[1]), str(host[2])))
          
        clientConn.send(("h"+str(hostList)).encode("utf-8"))
        return True
      
      if lead == "host":
        self.p2pHosts.append(client)
        return True
      
      if lead.split(":")[0] == "connect":
        print("client connected check")
        # hostUsr = clientConn.recv(2048).decode("utf-8")
        # p2pHost = filter(lambda x: x[2] == hostUsr, self.p2pHosts)
        # p2pHost[0].send("client_connected".encode("utf-8"))
        # time.sleep(1)
        # clientConn.send("connect".encode("utf-8"))
        # self.p2pHosts.remove(p2pHost)
        return True
        
      if lead == "disconnect":
        return None
      
      return lead
     
  def listen(self):
    try:
      for client in self.clients:
        message = self.getClientMessage(client)
        
        if not message:
          print("[DISCONNECTED] {}".format(client[2]))
          client[0].close()
          self.clients.remove(client)
          break
    
    except KeyboardInterrupt:
      print("\nClosing server...")
      self.server.close()
      print("Server closed.")
      sys.exit()
    
  def setClientHandle(self, client, handle):
    self.handle.append(handle)
    threading.Thread(target=handle, args=(client,)).start()
    
      

class TicTacToe:
  def __init__(self):
    self.board = [[0 for col in range(3)] for row in range(3)]
    self.players = ["X", "O"]
    self.turn = self.players[0]
    self.player1 = self.players[0]
    self.player2 = self.players[1]
    self.winner = None
    self.gamePlay = None
    self.gameOver = False
    
    self.counter = 0
    
  def hostGame(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    client, addr = server.accept()
    
    self.you = "X"
    self.opponent = "O"
    threading.Thread(target=self.handleConnect, args=(client,)).start()
    server.close()
    
  def connectGame(self, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    self.you = "O"
    self.opponent = "X"
    threading.Thread(target=self.handleConnect, args=(client,)).start()
    
  def handleComputer(self):
    print("\nGame starting...")
    self.displayBoard()
    
    while not self.gameOver:
      if self.turn == self.you:
        move = input("\nEnter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.opponent
        else:
          print("\nInvalid move.")
      else:
        print("\nComputer move:")
        self.makeMove(self.computerMove(), self.opponent)
        self.turn = self.you
    
  def handleConnect(self, client):
    print("\nConnected to opponent. Game starting...")
    self.displayBoard()
    
    while not self.gameOver:
      if self.turn == self.you:
        move = input("\nEnter move (row,column): ")
        if self.isValidMove(move.split(",")):
          client.send(move.encode("utf-8"))
          self.makeMove(move.split(","))
          self.turn = self.opponent
        else:
          print("\nInvalid move.")
      else:
        print("\nWaiting for opponent move...")
        data = client.recv(2048)
        if not data:
          client.close()
          break
        else:
          self.makeMove(data.decode("utf-8").split(","), self.opponent)
          self.turn = self.you
          
    client.close()
  
  def playHuman(self):
    print("\nGame starting...")
    self.gamePlay = "human"
    self.displayBoard()
    while not self.gameOver:
      if self.turn == self.player1:
        move = input("PLAYER 1: Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.player2
        else:
          print("Invalid move.")
      else:
        move = input("PLAYER 2: Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.player1
        else:
          print("Invalid move.")
  
  def playComputer(self):
    print("\nGame starting...")
    self.gamePlay = "computer"
    self.displayBoard()
    while not self.gameOver:
      if self.turn == self.player1:
        move = input("Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.player2
        else:
          print("Invalid move.")
      else:
        print("Computer move:")
        self.makeMove(self.computerMove())
        self.turn = self.player1
  
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
    self.displayBoard()
    
    if self.checkWinner():
      if self.winner == self.player1:
        if self.gamePlay == "computer":
          print("You win!")
        elif self.gamePlay == "human":
          print("Player 1 wins!")
        else:
          print("Player 1 wins!")
      elif self.winner == self.player2:
        if self.gamePlay == "computer":
          print("You lose!")
        elif self.gamePlay == "human":
          print("Player 2 wins!")
        else:
          print("Player 2 wins!")

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
  
  def displayBoard(self):
    for row in range(3):
      for col in range(3):
        if self.board[row][col] == 0:
          print(" ", end="")
        else:
          print(self.board[row][col], end="")
          
        if col < 2:
          print(" | ", end="")
        else:
          print()
          
      if row < 2:
        print("----------")
        

if __name__ == "__main__":
  try:
    server = Server()
    server.startServer()
  except KeyboardInterrupt:
    print("\nClosing server...")
    server.server.close()
    print("Server closed.")