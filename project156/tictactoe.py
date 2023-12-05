import pygame
import requests
import socket
import threading
import random
import sys
import re

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
        
class Game:
  def __init__(self):
    self.selection = None
    self.game = None
    self.host = None
    self.client = None
    
    while self.selection != "3":
      self.menuSelect()
      
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
      
  def menuSelect(self):
    print("\nSelect an option:")
    print("1. Play Offline")
    print("2. Connect to Server")
    print("3. Quit Game")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.menuGameSelectOffline()
    elif selection == "2":
      self.menuGameSelectOnline()
    elif selection == "3":
      print("Thank you for playing TicTacToe! Goodbye.")
      sys.exit()
    else:
      print("Invalid selection.")
      self.menuSelect()
    
  def menuGameSelectOffline(self):
    print("\nSelect an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.playComputer()
    elif selection == "2":
      self.playHuman()
    elif selection == "3":
      self.menuSelect()
    else:
      print("Invalid selection.")
      self.menuGameSelectOffline()
  
  def menuGameSelectOnline(self):
    print("\nSelect an option:")
    print("1. Play vs. Computer")
    print("2. Play vs. Human (Online)")
    print("3. Main Menu")
    
    selection = input("\nSelection: ")
    if selection == "1":
      self.game = TicTacToe()
      self.game.playComputer()
      
    elif selection == "2":
      self.game = TicTacToe()
      
      self.host = input("\nHost? (y/n): ")
      if self.host == "y":
        self.game.hostGame("localhost", 3333)
      else:
        self.game.connectGame("localhost", 3333)
        
      while not self.game.gameOver:
        pass
        
    elif selection == "3":
      self.playServer()
    elif selection == "4":
      self.playClient()
    elif selection == "5":
      sys.exit()
    else:
      print("Invalid selection.")
      self.menuSelect()
    
if __name__ == "__main__":
  game = Game()