import tkinter as tk
import tkinter.messagebox as mb
import random

from pygments.lexer import default

CELL_SIZE = 150
SIZE = CELL_SIZE * 3
board = [['', '', ''], ['', '', ''], ['', '', '']]
current_player = 'X'
game_mode = None

# ---------------- Grid ----------------
def grid(canvas):
    canvas["background"] = "black"
    for i in range(1, 3):
        canvas.create_line(CELL_SIZE * i, 0, CELL_SIZE * i, SIZE, fill="#99FFCC", width=4)
    for i in range(1, 3):
        canvas.create_line(0, CELL_SIZE * i, SIZE, CELL_SIZE * i, fill="#99FFCC", width=4)

# ---------------- Winner ----------------
def winner():
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

# ---------------- 2 Players Mode ----------------
def two_players_mode(event):
    global current_player
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE
    if board[row][col] == '':
        board[row][col] = current_player
        x_center = col * CELL_SIZE + CELL_SIZE / 2
        y_center = row * CELL_SIZE + CELL_SIZE / 2

        color = "#FFFF99" if current_player == "X" else "#FFCCFF"
        canvas.create_text(x_center, y_center, text=current_player, font=("Arial", CELL_SIZE // 2), fill=color)
    else:
        print("Cell already taken")
        return

    # Έλεγχος νίκης
    game_winner = winner()
    if game_winner:
        # mb.showinfo("Game Over", f"Player {game_winner} wins!")
        show_winner(f"Player {game_winner} wins!")

        canvas.unbind("<Button-1>")
        return

    # Έλεγχος ισοπαλίας
    is_draw = all(board[r][c] != '' for r in range(3) for c in range(3))
    if is_draw:
        # mb.showinfo("Game Over", "Draw!")
        show_winner("Draw!")

        canvas.unbind("<Button-1>")
        return

    current_player = 'O' if current_player == 'X' else 'X'

# ---------------- Restart ----------------
def restart_game():
    global board, current_player
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    current_player = 'X'
    canvas.delete("all")
    grid(canvas)
    # επαναφέρουμε το binding ανάλογα με το mode
    if game_mode == "2players":
        canvas.bind("<Button-1>", two_players_mode)
    else:
        canvas.bind("<Button-1>", player_vs_pc)


# ---------------- Result Window ----------------
def show_winner(winner_text):
    result_window = tk.Toplevel()
    result_window.title("Game Over")
    result_window.geometry("300x150")
    result_window.configure(bg="#222222")  # σκούρο background

    tk.Label(result_window, text=winner_text,
             font=("Arial", 20, "bold"),
             fg="#FFD700", bg="#222222").pack(pady=30)

    tk.Button(result_window, text="Restart", width=12,
              font=("Arial", 14, "bold"),
              bg="#3E3E44", fg="#C3F51E",
              activebackground="#ff2e63", activeforeground="white",
              relief="raised", bd=3,
              command=lambda: [restart_game(), result_window.destroy()]).pack(pady=10)


# ---------------- Minimax ----------------
def minimax(is_maximizing):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    result = winner()
    if result == 'O':
        return 1
    elif result == 'X':
        return -1
    elif not empty_cells:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for (i, j) in empty_cells:
            board[i][j] = 'O'
            score = minimax(False)
            board[i][j] = ''
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for (i, j) in empty_cells:
            board[i][j] = 'X'
            score = minimax(True)
            board[i][j] = ''
            best_score = min(best_score, score)
        return best_score

# ---------------- Easy / Medium / Hard ----------------
def easy_game():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if not empty_cells:
        return
    row, col = random.choice(empty_cells)
    board[row][col] = 'O'
    x_center = col * CELL_SIZE + CELL_SIZE / 2
    y_center = row * CELL_SIZE + CELL_SIZE / 2

    color_o = "#FFCCFF"

    canvas.create_text(x_center, y_center, text='O',
                       font=("Arial", CELL_SIZE // 2, "bold"),
                       fill=color_o)

def medium_game():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if not empty_cells:
        return
    for row, col in empty_cells:
        board[row][col] = 'O'
        if winner() == 'O':
            x_center = col * CELL_SIZE + CELL_SIZE / 2
            y_center = row * CELL_SIZE + CELL_SIZE / 2
            canvas.create_text(x_center, y_center, text='O', font=("Arial", CELL_SIZE // 2), fill="#FFCCFF")
            return
        board[row][col] = ''
    for row, col in empty_cells:
        board[row][col] = 'X'
        if winner() == 'X':
            board[row][col] = 'O'
            x_center = col * CELL_SIZE + CELL_SIZE / 2
            y_center = row * CELL_SIZE + CELL_SIZE / 2
            canvas.create_text(x_center, y_center, text='O', font=("Arial", CELL_SIZE // 2), fill="#FFCCFF")
            return
        board[row][col] = ''
    row, col = random.choice(empty_cells)
    board[row][col] = 'O'
    x_center = col * CELL_SIZE + CELL_SIZE / 2
    y_center = row * CELL_SIZE + CELL_SIZE / 2
    canvas.create_text(x_center, y_center, text='O', font=("Arial", CELL_SIZE // 2), fill="#FFCCFF")

def hard_game():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    best_score = -float("inf")
    move = None
    for i, j in empty_cells:
        board[i][j] = 'O'
        score = minimax(False)
        board[i][j] = ''
        if score > best_score:
            best_score = score
            move = (i, j)
    if move:
        row, col = move
        board[row][col] = 'O'
        x_center = col * CELL_SIZE + CELL_SIZE / 2
        y_center = row * CELL_SIZE + CELL_SIZE / 2
        canvas.create_text(x_center, y_center, text='O', font=("Arial", CELL_SIZE // 2), fill="#FFCCFF")

# ---------------- Player vs PC ----------------
def player_vs_pc(event):
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE
    if board[row][col] != '':
        print("Cell already taken!")
        return

    # Παίκτης X
    board[row][col] = 'X'
    x_center = col * CELL_SIZE + CELL_SIZE / 2
    y_center = row * CELL_SIZE + CELL_SIZE / 2
    canvas.create_text(x_center, y_center, text='X', font=("Arial", CELL_SIZE // 2), fill="#FFFF99")

    game_winner = winner()
    if game_winner:
        # mb.showinfo("Game Over", f"Player {game_winner} wins!")
        show_winner(f"Player {game_winner} wins!")

        canvas.unbind("<Button-1>")
        return

    is_draw = all(board[r][c] != '' for r in range(3) for c in range(3))
    if is_draw:
        # mb.showinfo("Game Over", "Draw!")
        show_winner("Draw!")

        canvas.unbind("<Button-1>")
        return

    # Κίνηση υπολογιστή με καθυστέρηση
    if game_mode == "easy":
        canvas.after(300, easy_game)
    elif game_mode == "medium":
        canvas.after(300, medium_game)
    elif game_mode == "hard":
        canvas.after(300, hard_game)

    # Έλεγχος νίκης μετά τον υπολογιστή
    def check_after_pc():
        game_winner = winner()
        if game_winner:
            # mb.showinfo("Game Over", f"Player {game_winner} wins!")
            show_winner(f"Player {game_winner} wins!")

            canvas.unbind("<Button-1>")
            return
        is_draw = all(board[r][c] != '' for r in range(3) for c in range(3))
        if is_draw:
            # mb.showinfo("Game Over", "Draw!")
            show_winner("Draw!")

            canvas.unbind("<Button-1>")
    canvas.after(350, check_after_pc)

# ---------------- Main Game Window ----------------
def start_main_game(selected_mode, mode_window):
    global game_mode, canvas
    game_mode = selected_mode
    mode_window.destroy()

    main_window = tk.Tk()
    main_window.title("Tic Tac Toe Game")

    canvas = tk.Canvas(main_window, width=SIZE, height=SIZE)
    canvas.pack()
    grid(canvas)

    restart_button = tk.Button(main_window,
                    text="Restart",
                    width=15,
                    font=("Arial",14,"bold"),
                    bg="#99FFCC",
                    fg="black",
                    activebackground="#3E3E44",
                    activeforeground="white",
                    relief="raised", bd=3,
                    command=restart_game
                               )

    restart_button.pack(pady=10)

    if game_mode == "2players":
        canvas.bind("<Button-1>", two_players_mode)
    else:
        canvas.bind("<Button-1>", player_vs_pc)

    main_window.mainloop()

def add_hover_effect(button, hover_bg="black"):
    default_bg=button['bg']
    def on_enter(e):
        e.widget['background'] = hover_bg

    def on_leave(e):
        e.widget['background'] = default_bg

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def style_button(button, hover_bg="black"):
    """
    Προσθέτει hover effect και pointer cursor σε ένα κουμπί.
    - hover_bg: χρώμα όταν περνάει το ποντίκι
    Το αρχικό background παίρνεται αυτόματα από το button.
    """
    default_bg = button['bg']  # παίρνει το αρχικό χρώμα

    # hover effect
    def on_enter(e):
        e.widget['background'] = hover_bg

    def on_leave(e):
        e.widget['background'] = default_bg

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    # pointer cursor
    button.config(cursor="hand2")



# ---------------- Initial Mode Selection ----------------
mode_window = tk.Tk()
mode_window.title("Choose Game Mode")
mode_window.configure(bg="#070901")
tk.Label(mode_window, text="Select Game Mode:", font=("Arial", 18,"bold"),fg="black",bg="#783AF5").pack(pady=20,padx=20)

btn_2players=tk.Button(mode_window,
          text="2 Players",
          width=15,
          command=lambda: start_main_game("2players", mode_window),
          bg = "#3E3E44", fg = "#C3F51E",
          font = ("Arial", 14, "bold"),
          activebackground = "#ff2e63", activeforeground = "white",
          relief = "raised",
          bd = 3,
          )
btn_2players.pack(pady=10)
add_hover_effect(btn_2players)
style_button(btn_2players)


btn_easy=tk.Button(mode_window,
          text="Easy",
          width=15,
          command=lambda: start_main_game("easy", mode_window),
          bg="#3E3E44", fg="#C3F51E",
          font=("Arial", 14, "bold"),
          activebackground="#ff2e63", activeforeground="white",
          relief="raised", bd=3
          )
btn_easy.pack(pady=10)
add_hover_effect(btn_easy)
style_button(btn_easy)

btn_medium=tk.Button(mode_window,
          text="Medium",
          width=15,
          command=lambda: start_main_game("medium", mode_window),
          bg="#3E3E44", fg="#C3F51E",
          font=("Arial", 14, "bold"),
          activebackground="#ff2e63", activeforeground="white",
          relief="raised", bd=3
          )
btn_medium.pack(pady=10)
add_hover_effect(btn_medium)
style_button(btn_medium)

btn_hard=tk.Button(mode_window,
          text="Hard",
          width=15,
          command=lambda: start_main_game("hard", mode_window),
          bg="#3E3E44", fg="#C3F51E",
          font=("Arial", 14, "bold"),
          activebackground="#ff2e63", activeforeground="white",
          relief="raised", bd=3
          )
btn_hard.pack(pady=10)
add_hover_effect(btn_hard)
style_button(btn_hard)


mode_window.mainloop()
