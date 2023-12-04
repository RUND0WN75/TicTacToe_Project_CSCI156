import socket
import time
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
port = 8080
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()

def send_board():
    board_str = str(board)
    for conn in playerConn:
        conn.send("Matrix".encode())
        time.sleep(1)
        conn.send(board_str.encode())

def send_msg(message):
    for conn in playerConn:
        conn.send(message.encode())

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        conn = playerConn[0]
    else:
        player = "Player Two's Turn"
        conn = playerConn[1]

    print(player)

    send_msg(player)

    try:
        conn.send("Input".encode())
        data = conn.recv(2048*10)
        conn.settimeout(20)
        data_decoded = data.decode().split(",")
        x = int(data_decoded[0])
        y = int(data_decoded[1])

        board[x][y] = currentPlayer
        send_board()
        #send_common_msg("Matrix")
        #send_common_msg(str(board))
    except:
        conn.send("Error".encode())
        print("Error")

def check_win(board):
    # check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return True

    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return True

    # check negative diagonal
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return True

    #check positive diagonal
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return True

    return False

def start_server():
    try:
        server.bind((host, port))
        print("The server for CSCI 156 Project Group 4 has started")
        server.listen(2)
        accept_players()

    except socket.error as e:
        print("Error", e)

def accept_players():
    try:
        for i in range(2):
            conn, addr = server.accept()
            msg1 = "<<< You are player {} >>>".format(i+1)
            conn.send(msg1.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))

        start_game()
        server.close()
    except socket.error as e:
        print("Error", e)

def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9:
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_win(board)
        i += 1
    
    send_msg("Over")

    if result == 1:
        #screen_board(board)
        #screen_board(board, "Player 1 wins", 3000)
        #running = False
        win_mssg = "Player 1 wins"
    elif result == 2:
        #screen_board(board)
        #screen_board(board, "Player 2 wins", 3000)
        #running = False
        win_mssg = "Player 2 wins"

    elif all(cell != 0 for row in board for cell in row):
        #screen_board(board)
        #screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
        #running = False
        win_mssg = "Game ended in a draw. Better luck next time"
    else:
        win_mssg = "Error"
        #computer_move(board)
        #if check_win(board):
         #   screen_board(board)
          #  screen_board(board, "Computer won the game. Better luck next time.", 3000)
           # running = False
        #elif all(cell != 0 for row in board for cell in row):
         #   screen_board(board, "Game ended in a draw. Better luck next time.", 3000)
          #  running = False
    #screen_board(board)

    send_msg(win_mssg)
    time.sleep(15)

    for conn in playerConn:
        conn.close()


#def send_common_msg(message):
 #   playerConn[0].send(message.encode())
  #  playerConn[1].send(message.encode())
   # time.sleep(15)


start_server()
