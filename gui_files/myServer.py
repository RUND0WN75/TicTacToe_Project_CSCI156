import socket
import time

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
        conn.send(board_str.encode())

def send_msg(message):
    for conn in playerConn:
        conn.send(message.encode())

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Turn of Player One"
        conn = playerConn[0]
    else:
        player = "Turn of Player Two"
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
        send_msg("Matrix")
        send_msg(str(board))
    except:
        conn.send("Error".encode())
        print("Error")

def check_win(board):
    winner = 0
    # check rows
    for i in range(3):
       if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            winner = board[i][0]
            if winner != 0:
                break
    
    #check columns
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            winner = board[0][i]
            if winner != 0:
                break

    #check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        winner = board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        winner = board[0][2]
        
    return winner

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
    current_player = playerOne

    while result == 0 and i < 9:
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_win(board)
        i += 1
        if current_player == playerOne:
            current_player = playerTwo 
        else:
            current_player = playerOne
    

    if result == 1:
        win_mssg = "Game won by Player 1"
    elif result == 2:
        win_mssg = "Game won by Player 2"

    elif all(cell != 0 for row in board for cell in row):
        win_mssg = "Game ended in a draw. Better luck next time"
    else:
        win_mssg = "Error"

    send_msg(win_mssg)
    time.sleep(2)
    send_msg("Over")
    
    time.sleep(10)

    for conn in playerConn:
        conn.close()

start_server()
