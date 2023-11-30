#include <iostream>
using std::cin;
using std::cout;
using std::endl;

void PlayerIn (int board[][3]) {
int r, c;
cout << "Enter row:" << endl;
cin >> r;
cout << "Enter column:" << endl;
cin >> c;

//check that the cell is not in use
while (board[r-1][c-1] != 0) {
    cout << "Cell already taken. Please try again." << endl;
    cout << "Enter row:" << endl;
    cin >> r;
    cout << "Enter column:" << endl;
    cin >> c;
}

//place
board[r-1][c-1] = 1;
}

void ComputerMove(int board[][3]) {
int r, c;
r = rand() % 3;
c = rand() % 3;

//if the place is already taken, reroll
while (board[r][c] != 0){
r = rand() % 3;
c = rand() % 3;
}

board [r][c] = 2;
cout << "Computer played O at Row: " << r + 1 << " Column: " << c + 1 << endl; 
}

bool CheckWin(int board[][3]) {
//check rows    
for (int i = 0; i < 3; i++) {
    if (board[i][0] == board[i][1] && board[i][0] == board[i][2] && board[i][0] != 0) {
        return true;
    }
}
//check columns
for (int i = 0; i < 3; i++) {
    if (board[0][i] == board[1][i] && board[0][i] == board[2][i] && board[i][0] != 0) {
        return true;
    }
}
//check negative diagonal
if (board[0][0] == board[1][1] && board[0][0] == board[2][2] && board[0][0] != 0){
    return true;
}
//check positive diagonal
if (board[0][2] == board[1][1] && board[0][2] == board[2][0] && board[0][2] != 0){
    return true;
}
return false;
}

void ResetBoard(int board[][3]) {
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++)
    board[i][j] = 0;
}
}

void DisplayBoard(int board[][3]) {
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        switch (board[i][j])
        {
        case 0:
            cout << ' ';
            break;
        case 1: 
            cout << 'X';
            break;
        case 2:
            cout << 'O';
            break;
        default:
            break;
        }
        if (j < 2) {
            cout << '|';
        }
        else  {
            cout << endl;
        }
    }
    if (i < 2) {
        cout << "-----" << endl;
    }
    
}

}



int main() {

//board uses a 2D array implementation
int board [3][3];


cout << "Player is X, Computer is O" << endl;

ResetBoard(board);
bool check = true;

for (int i = 0; i < 9; i++) {
PlayerIn(board);
if (CheckWin(board)) {
    DisplayBoard(board);
    cout << "Congratulations: You won the game!" << endl;
    break;
}
ComputerMove(board);
if (CheckWin(board)) {
    DisplayBoard(board);
    cout << "Computer won the game. Better luck next time." << endl;
    break;
}
    
if (i == 8 && CheckWin(board) == false) {
    cout << "Game ended in a draw. Better luck next time" << endl;
}
DisplayBoard(board);
}


return 0;
}
