from os import system, name
import pygame
import requests
import socket
import threading
import random
import sys
import re
import ast

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

class Client:
  def __init__(self, host):
    self.host = host
    self.port = 3333
    self.addr = None
    self.addrPort = None
    self.handle = ""
    
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((self.host, self.port))
    self.addr, self.addrPort = self.client.getsockname()
    
    handle = input("Enter your username: ")
    self.client.send('handle'.encode("utf-8"))
    self.client.send(handle.encode("utf-8"))
    self.handle = handle
  
    self.running = True
    
    # self.threadCreation(self.msgAccept)
    
  def msgAccept(self):
    while self.running:
      if not self.running:
        return None
      if not self.client:
        return None
      try: 
        data = self.client.recv(1024)
        if not data:
          self.client.close()
          break
        else:
          lead = data.decode("utf-8")

          if lead == "clients":
            clients = self.client.recv(1024).decode("utf-8")
            return clients
          
          elif lead[0] == "h":
            
            global hosts
            try: 
              hosts = eval(lead[1:])
              
            except: 
              hosts = lead[1:]
            
            return hosts
          
          elif lead == "connect":
            return True
          
          elif lead == "client_connected":
            return True
          
          return lead
      except Exception as e:
        print(e)
        
  def threadCreation(self, target):
    threading.Thread(target=target).start()
    
  def sendMsg(self, msg):
    print(msg.encode("utf-8"))
    self.client.send(msg.encode("utf-8"))
    
  def close(self):
    self.running = False
    self.client.close()
    
  def disconnect(self):
    self.sendMsg("disconnect")
    self.close()
     
class Game:
  def __init__(self):
    self.selection = None
    self.game = None
    self.host = None
    self.client = None
    
    while self.selection != "3":
      self.menuSelect()
      
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
    
  def playHuman(self):
    self.game = TicTacToe()
    self.game.playHuman()
    
    while not self.game.gameOver:
      pass
  
  def playP2P(self):
    self.game = TicTacToe()
      
    self.host = input("\nHost? (y/n): ")
    if self.host == "y":
      self.game.hostGame("localhost", 3333)
    else:
      self.game.connectGame("localhost", 3333)
      
    while not self.game.gameOver:
      pass
      
  def get_external_ip():
    # Make a request to checkip.dyndns.org as proposed
    # in https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery#DNS_Addresses
    response = requests.get('http://checkip.dyndns.org').text
 
    # Filter the response with a regex for an IPv4 address
    ip = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response).group()
    return ip
  
  def menuPlayerSelect(self):
    self.client.sendMsg("hosts")
    hosts = self.client.msgAccept()
      
    print("Select an option:")
    print("1. Host Game (Player 1)")
    print("2. Join Game (Player 2)")
    
    selection = input("\nSelection: ")
    
    if (selection == "1"):
      self.client.sendMsg("host")
      print("Waiting for another player to connect...")
      
      connected = self.client.msgAccept()
      if connected:
        self.game.hostGame(self.client.addr, 8888)
        self.client.sendMsg("active")
        
        while not self.game.gameOver:
          pass
        
    if (selection == "2"):
      if len(hosts) == 0:
        print("\nNo hosts available. Host a game? (y/n): ")
        selection = input("\nSelection: ")
        if selection == "y":
          self.client.sendMsg("host")
          print("Waiting for another player to connect...")
          
          connected = self.client.msgAccept()
          if connected == "client_connected":
            self.game.hostGame(self.client.addr, 8888)
            
            while not self.game.gameOver:
              pass
            
        else:
          print("Try again later.")
          print("\n")
          self.menuGameSelectOnline()
      
      else:
        print('Select an opponent:')
        for idx, host in enumerate(hosts):
          print(str(idx + 1) + ". " + host[2])
        
        selection = input("\nSelection: ")
        
        isNum = selection.isnumeric()
        if isNum and int(selection) <= 9:
          selectedHost = hosts[int(selection) - 1]
          usr = selectedHost[2]
          
          self.client.sendMsg("connect:"+usr)
          connected = self.client.msgAccept()
          print(connected+" connected")
          
          if connected:
            self.game.connectGame(host[1].split(":")[0], int(host[1].split(":")[1]))
            
            while not self.game.gameOver:
              pass
        else:
          if int(selection) == 0:
            self.menuGameSelectOnline()
          else:
            print("Invalid selection.")
            print("\n")
            self.menuPlayerSelect()
      
  def menuSelect(self):
    print("hello"[0])
    print("Welcome to TicTacToe!")
    print("\nSelect an option:")
    print("1. Play Offline")
    print("2. Connect to Server")
    print("3. Quit Game")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.clear()
      self.menuGameSelectOffline()
    elif selection == "2":
      self.clear()
      serverIP = input("Enter the server IP to connect: ")
      self.client = Client(serverIP)
      print("\nConnected as " + self.client.handle)
      
      self.menuGameSelectOnline()
    elif selection == "3":
      self.clear()
      print("Thank you for playing TicTacToe! Goodbye.")
      sys.exit()
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.menuSelect()
    
  def menuGameSelectOffline(self):
    print("Select an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.clear()
      self.playComputer()
    elif selection == "2":
      self.clear()
      self.playHuman()
    elif selection == "3":
      self.clear()
      self.menuSelect()
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.menuGameSelectOffline()
  
  def menuGameSelectOnline(self):
    print("Select an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human (Online)")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.clear()
      self.playComputer()
      
    elif selection == "2":
      self.clear()
      self.menuPlayerSelect()
        
    elif selection == "3":
      self.client.sendMsg("disconnect")
      self.client.disconnect()
      self.clear()
      self.menuSelect()
    else:
      self.clear()
      print("Invalid selection.")
      print("\n")
      self.menuGameSelectOnline()
    
if __name__ == "__main__":
  game = Game()
  