from os import system, name
import socket
import random
import threading
import sys

# Class to represent a client that has the pattern of send message
# and receive message in the same order
class Client:
  def __init__(self, host):
    self.host = host
    self.port = 3333
    self.connected = False
    self.client = None
    self.addr = None
    self.handle = None
    
    self.connect()
    
  def sendMessage(self, msg):
    self.client.send(msg.encode("utf-8")[:1024])
    
  def receiveMessage(self):
    server_response = self.client.recv(1024).decode("utf-8")
    lead = server_response.split("::")[0]
    
    match lead.lower():
      case "connected":
        client_addr = server_response.split("::")[1]
        self.addr = eval(client_addr)
        return "connected"
      case "move":
        return eval(server_response.split("::")[1])
      case "hosts":
        hosts = eval(server_response.split("::")[1])
        return hosts
      case _:
        return lead
    
  def connect(self):
    self.connected = False
    while not self.connected:
      try:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        response = self.receiveMessage()
        if response == "connected":
          self.connected = True
      except Exception as e:
        print(f"Error: {e}")
      
  def close(self):
    # close client socket (connection to the server)
    self.client.close()
    print("Connection to server closed")
   
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
    
  def hostGame(self, host, port, handle):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    client, addr = server.accept()
    
    self.you = "X"
    self.opponent = "O"
    self.player1 = handle
    threading.Thread(target=self.handleConnect, args=(client,)).start()
    server.close()
    
  def connectGame(self, host, port, handle):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    self.you = "O"
    self.opponent = "X"
    self.player2 = handle
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
        data = client.recv(1024)
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
      if self.turn == self.players[0]:
        move = input(f"{self.player1}: Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.players[1]
        else:
          print("Invalid move.")
      else:
        move = input(f"{self.player2}: Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.players[0]
        else:
          print("Invalid move.")
  
  def playComputer(self):
    print("\nGame starting...")
    self.gamePlay = "computer"
    self.displayBoard()
    while not self.gameOver:
      if self.turn == self.players[0]:
        move = input("Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          self.makeMove(move.split(","))
          self.turn = self.players[1]
        else:
          print("Invalid move.")
      else:
        print("Computer move:")
        self.makeMove(self.computerMove())
        self.turn = self.players[0]
        
  def playComputerOnline(self, client):
    client.sendMessage("ping")
    response = client.receiveMessage()
    
    if response == "pong":
      print("\nGame starting...")
      self.gamePlay = "computer"
      self.displayBoard()
      
    else:
      print("Error: Could not connect to server.")
      print("\n")
      return
      
    while not self.gameOver:
      if self.turn == self.players[0]:
        move = input("Enter move (row,column): ")
        if self.isValidMove(move.split(",")):
          client.sendMessage(f"move::{str(move)}")
          self.makeMove(move.split(","))
          self.turn = self.players[1]
        else:
          print("Invalid move.")
      else:
        print("Computer move:")
        waiting = True
        while waiting:
          move = client.receiveMessage()
          waiting = False
          self.makeMove(move)
          self.turn = self.players[0]
          
    client.sendMessage("game_over")
      
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
    self.clear()
    self.displayBoard()
    
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

  def clear(self):
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
class Game:
  def __init__(self):
    self.selection = None
    self.game = None
    self.host = None
    self.client = None
    self.p2pPort = 8888
    
    while self.selection != "3":
      self.mainMenu()
    
  def clear(self):
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
  def playComputer(self):
    self.game = TicTacToe()
    self.game.playComputer()
    
    while not self.game.gameOver:
      pass
    
  def playComputerOnline(self, client):
    self.game = TicTacToe()
    self.game.playComputerOnline(client)
    
    while not self.game.gameOver:
      pass  
  
  def playHuman(self):
    self.game = TicTacToe()
    self.game.playHuman()
    
    while not self.game.gameOver:
      pass
        
  def mainMenu(self):
    print("Welcome to TicTacToe!")
    print("\nSelect an option:")
    print("1. Play Offline")
    print("2. Connect to Server")
    print("3. Quit Game")
    
    selection = input("\nSelection: ")
    
    if selection == "1":
      self.clear()
      self.offlineMenu()
      
    elif selection == "2":
      self.clear()
      serverIP = input("Enter the server IP Address to connect: ")
      self.client = Client(serverIP)
      
      handle = input("Enter your username: ")
      while handle == "":
        handle = input("Enter your username: ")
        
      self.client.sendMessage(f'handle::{handle}')
      response = self.client.receiveMessage()
      
      if response == "accepted":
        self.client.handle = handle
        print("\nConnected as " + handle)
        self.onlineMenu()
        
      else:
        print("Error: Username already taken.")
        self.mainMenu()
      
    elif selection == "3":
      self.clear()
      print("Thank you for playing TicTacToe! Goodbye.")
      sys.exit()
      
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.mainMenu()
     
  def onlineMenu(self):
    print("Select an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human (Online)")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    
    if selection == "1":
      self.clear()
      try:
        self.playComputerOnline(self.client)
      except Exception as e:
        print(e)
        print("Error: Could not connect to server.")
        print("\n")
        self.onlineMenu()
      
      print("\nGame over. Returning to game menu...\n")
      self.onlineMenu()
      
    elif selection == "2":
      self.clear()
      self.playerSelectMenu()
        
    elif selection == "3":
      self.client.sendMessage("close")
      self.client.client.close()
      self.clear()
      self.mainMenu()
      
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.onlineMenu()
      
  def playerSelectMenu(self):
    print("Select an option:")
    print("1. Host Game (Player 1)")
    print("2. Join Game (Player 2)")
    print("3. Game Menu")
    
    selection = input("\nSelection: ")
    
    if selection == "1":
      self.client.sendMessage(f"host::{self.p2pPort}")
      print("Waiting for another player to connect...")
      waiting = True
      while waiting:
        response = self.client.receiveMessage()
      
        if response == "player_connected":
          waiting = False
          print("Player 2 has connected!")
          self.client.sendMessage("host_active")
          self.game = TicTacToe()
          self.game.hostGame(self.client.addr[0], self.p2pPort, self.client.handle)
          
          while not self.game.gameOver:
            pass
          
          print("\nGame over. Returning to game menu...\n")
          self.onlineMenu()
      
    elif selection == "2":
      self.client.sendMessage("hosts")
      hosts = self.client.receiveMessage()
      print(hosts)
      
      if len(hosts) == 0:
        print("\nNo hosts available. Host a game? (y/n): ")
        selection = input("\nSelection: ")
        
        if selection == "y":
          self.client.sendMessage(f"host::{self.p2pPort}")
          print("Waiting for another player to connect...")
          waiting = True
          while waiting:
            response = self.client.receiveMessage()
              
            if response == "player_connected":
              waiting = False
              print("Player 2 has connected!")
              self.client.sendMessage("host_active")
              # response = self.client.receiveMessage()
              if response == "accepted":
                self.game = TicTacToe()
                self.game.hostGame(self.addr[0], self.p2pPort, self.client.handle)
                
                while not self.game.gameOver:
                  pass
                
              print("\nGame over. Returning to game menu...\n")
              self.onlineMenu()
        else:
          print("Try again later.")
          print("\n")
          self.onlineMenu()
          
      else:
        print('Select an opponent:')
        for idx, host in enumerate(hosts):
          print(str(idx + 1) + ". " + host[0])
        
        selection = input("\nSelection: ")
        
        isNum = selection.isnumeric()
        if isNum and int(selection) <= 9:
          selectedHost = hosts[int(selection) - 1]
          self.client.sendMessage(f'connect::{str(selectedHost)}')
          waiting = True
          while waiting:
            response = self.client.receiveMessage()
          
            if response == "player_connected":
              waiting = False
              print("Connected to host!")
              self.game = TicTacToe()
              self.game.connectGame(selectedHost[1][0], int(selectedHost[1][1]), self.client.handle)
              
              while not self.game.gameOver:
                pass
              
            print("\nGame over. Returning to game menu...\n")
            self.onlineMenu()
          else:
            print("Error: Could not connect to host.")
            print("\n")
            self.onlineMenu()
      
    elif selection == "3":
      self.clear()
      self.onlineMenu()
      
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.playerSelectMenu()
      
  def offlineMenu(self):
    print("Select an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    
    if selection == "1":
      self.clear()
      self.playComputer()
      
      print("\nGame over. Returning to game menu...\n")
      self.offlineMenu()
      
    elif selection == "2":
      self.clear()
      self.playHuman()
      
      print("\nGame over. Returning to game menu...\n")
      self.offlineMenu()
      
    elif selection == "3":
      self.clear()
      self.mainMenu()
      
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.offlineMenu()

if __name__ == "__main__":
  game = Game()