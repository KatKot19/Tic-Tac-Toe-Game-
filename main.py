import tkinter as tk
import tkinter.messagebox as mb
import random

CELL_SIZE=150
SIZE=CELL_SIZE*3
board = [
  ['', '', ''],
  ['', '', ''],
  ['', '', '']
]

current_player = 'X'
game_mode="easy"

def grid(canvas):
    canvas["background"] = "black"
    for i in range(1,3):
        canvas.create_line(CELL_SIZE*i, 0, CELL_SIZE*i, SIZE, fill="#99FFCC", width=4)
    for i in range(1,3):
        canvas.create_line(0, CELL_SIZE*i, SIZE, CELL_SIZE*i, fill="#99FFCC", width=4)

def winner():
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]  # νικητής

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]  # νικητής

    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]


    return None  # κανένας νικητής

def two_players_mode(event): #adapted to rows and columns instead of pixels

    global current_player

    row=event.y//CELL_SIZE
    col=event.x//CELL_SIZE

    if board[row][col]=='':
        board[row][col]=current_player

        x_center=col*CELL_SIZE+CELL_SIZE/2
        y_center = row * CELL_SIZE + CELL_SIZE / 2

        canvas.create_text(x_center, y_center,
                           text=current_player,
                           font=("Arial", CELL_SIZE//2),
                           fill="white")

    else:
        print("Cell already taken")

    print(f"click on cell:{row},{col}")

    # έλεγχος νίκης
    game_winner = winner()
    if game_winner:
        mb.showinfo("Game Over", f"Player {game_winner} wins!")
        canvas.unbind("<Button-1>")
        return

    # έλεγχος ισοπαλίας
    is_draw = all(board[row][col] != '' for row in range(3) for col in range(3))
    if is_draw:
        mb.showinfo("Game Over", "Draw!")
        canvas.unbind("<Button-1>")

    current_player = 'O' if current_player == 'X' else 'X'


def restart_game():
    global board,current_player
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    current_player = 'X'
    canvas.delete("all")  # καθαρίζει όλα τα σχέδια
    grid(canvas)  # ξανασχεδιάζει το grid
    canvas.bind("<Button-1>", two_players_mode)  # ενεργοποιεί ξανά τα κλικ



def easy_game():

    empty_cells=[]

    for i in range(0,3):
        for j in range(0,3):
            if board[i][j]=='':
                empty_cells.append((i,j))

    if not empty_cells:
        return

    pc_choice=random.choice(empty_cells)
    row,col=pc_choice

    board[row][col]='O'

    x_center = col * CELL_SIZE + CELL_SIZE / 2
    y_center = row * CELL_SIZE + CELL_SIZE / 2

    canvas.create_text(x_center, y_center,
                       text='O',
                       font=("Arial", CELL_SIZE // 2),
                       fill="white")

def medium_game():
    empty_cells = []

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '':
                empty_cells.append((i, j))

    if not empty_cells:
        return

    for row in board:
        if row[0]==row[1]:
            board[row][2]='O'
        elif row[0]==row[2]:
            board[row][1]='O'
        elif row[1]==row[2]:
            board[row][0]='O'

    for col in range(3):
         if board[0][col] == board[1][col]:
             board[2][col]='O'
         elif board[0][col] == board[2][col]:
                board[1][col]='O'
         elif board[2][col] == board[1][col]:
             board[0][col]='O'

    if board[0][0]==board[1][1]=='O':
        board[2][2]='O'
    elif board[0][0]==board[2][2]=='O':
        board[1][1]='O'
    elif board[2][2]==board[1][1]=='O':
        board[1][1]='O'









def hard_game():
    pass


def player_vs_pc(event):
    player='X'
    pc='O'
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE

    if board[row][col]=='':
        board[row][col]=player
        x_center = col * CELL_SIZE + CELL_SIZE / 2
        y_center = row * CELL_SIZE + CELL_SIZE / 2
        canvas.create_text(x_center, y_center,
                           text=player,
                           font=("Arial", CELL_SIZE//2),
                           fill="white")
    else:
        print("Cell already taken!")
        return

    if game_mode=="easy":
        easy_game()
    elif game_mode=="medium":
        medium_game()
    else:
        hard_game()







window=tk.Tk()
window.title("Tic Tac Toe Game")

canvas=tk.Canvas(window,width=SIZE,height=SIZE)
canvas.pack()

grid(canvas)

canvas.bind("<Button-1>",two_players_mode)
restart_button = tk.Button(window, text="Restart", command=restart_game)
restart_button.pack(pady=10)






window.mainloop()