import tkinter as tk
from tkinter import messagebox

# =========================================================
# COLOR PALETTE (Dark theme — matches CodSoft project styling)
# =========================================================
COLOR_BG        = "#0f1117"   # app background
COLOR_PANEL     = "#171a23"   # board panel
COLOR_CELL      = "#1d2129"   # empty cell
COLOR_CELL_HOV  = "#272b36"   # cell hover
COLOR_X         = "#3da9fc"   # human marker (blue)
COLOR_O         = "#e63946"   # AI marker (red)
COLOR_TEXT      = "#f1f1f4"
COLOR_TEXT_DIM  = "#9098a8"
COLOR_BORDER    = "#272b36"
COLOR_WIN       = "#4ade80"

FONT_FAMILY = "Segoe UI"

# --------------------------
# Game Logic (unchanged)
# --------------------------

board = [" " for _ in range(9)]

human = "X"
ai = "O"


def check_winner(brd, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for condition in win_conditions:
        if all(brd[i] == player for i in condition):
            return condition

    return None


def is_draw(brd):
    return " " not in brd


def minimax(brd, depth, maximizing):

    if check_winner(brd, ai):
        return 1

    if check_winner(brd, human):
        return -1

    if is_draw(brd):
        return 0

    if maximizing:
        best_score = -float("inf")
        for i in range(9):
            if brd[i] == " ":
                brd[i] = ai
                score = minimax(brd, depth + 1, False)
                brd[i] = " "
                best_score = max(score, best_score)
        return best_score

    else:
        best_score = float("inf")
        for i in range(9):
            if brd[i] == " ":
                brd[i] = human
                score = minimax(brd, depth + 1, True)
                brd[i] = " "
                best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -float("inf")
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            score = minimax(board, 0, False)
            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


# =========================================================
# GUI STATE
# =========================================================
game_over = False
x_score = 0
o_score = 0
draw_score = 0


# =========================================================
# GUI Functions
# =========================================================
def highlight_win(condition, color):
    for i in condition:
        buttons[i].config(bg=color, fg="white")


def end_game(message, color):
    global game_over
    game_over = True
    set_status(message, color)
    disable_board()


def update_scoreboard():
    score_label.config(
        text=f"You  {x_score}      AI  {o_score}      Draws  {draw_score}"
    )


def set_status(text, color=COLOR_TEXT_DIM):
    status_label.config(text=text, fg=color)


def ai_turn():
    global o_score

    set_status("AI is thinking…", COLOR_TEXT_DIM)
    root.update_idletasks()

    move = best_move()

    if move is not None:
        board[move] = ai
        buttons[move]["text"] = ai
        buttons[move].config(fg=COLOR_O)
        buttons[move]["state"] = "disabled"

    win = check_winner(board, ai)
    if win:
        o_score += 1
        update_scoreboard()
        highlight_win(win, COLOR_O)
        end_game("AI wins this round.", COLOR_O)
        return

    if is_draw(board):
        global draw_score
        draw_score += 1
        update_scoreboard()
        end_game("It's a draw.", COLOR_TEXT_DIM)
        return

    set_status("Your move — tap a cell.", COLOR_X)


def player_move(index):
    global x_score

    if game_over or board[index] != " ":
        return

    board[index] = human
    buttons[index]["text"] = human
    buttons[index].config(fg=COLOR_X)
    buttons[index]["state"] = "disabled"

    win = check_winner(board, human)
    if win:
        x_score += 1
        update_scoreboard()
        highlight_win(win, COLOR_X)
        end_game("You win! 🎉", COLOR_X)
        return

    if is_draw(board):
        global draw_score
        draw_score += 1
        update_scoreboard()
        end_game("It's a draw.", COLOR_TEXT_DIM)
        return

    ai_turn()


def disable_board():
    for btn in buttons:
        btn["state"] = "disabled"


def reset_game():
    global board, game_over

    board = [" " for _ in range(9)]
    game_over = False

    for btn in buttons:
        btn["text"] = ""
        btn["state"] = "normal"
        btn.config(bg=COLOR_CELL, fg=COLOR_TEXT)

    set_status("Your move — tap a cell.", COLOR_X)


def on_cell_enter(event, idx):
    if board[idx] == " " and not game_over:
        event.widget.config(bg=COLOR_CELL_HOV)


def on_cell_leave(event, idx):
    if board[idx] == " " and not game_over:
        event.widget.config(bg=COLOR_CELL)


def style_button(btn, bg, hover_bg, fg="white"):
    btn.config(
        bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
        relief="flat", bd=0, font=(FONT_FAMILY, 11, "bold"),
        cursor="hand2", padx=14, pady=8
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))


# =========================================================
# GUI BUILD
# =========================================================
root = tk.Tk()
root.title("Tic Tac Toe AI — Unbeatable Minimax")
root.geometry("440x640")
root.configure(bg=COLOR_BG)
root.resizable(False, False)

# ---- Header ----
header_frame = tk.Frame(root, bg=COLOR_BG)
header_frame.pack(fill="x", padx=30, pady=(28, 0))

title_label = tk.Label(
    header_frame,
    text="⭕ Tic Tac Toe",
    font=(FONT_FAMILY, 24, "bold"),
    bg=COLOR_BG, fg=COLOR_TEXT
)
title_label.pack(anchor="w")

subtitle_label = tk.Label(
    header_frame,
    text="Powered by the Minimax algorithm — the AI never loses.",
    font=(FONT_FAMILY, 10),
    bg=COLOR_BG, fg=COLOR_TEXT_DIM
)
subtitle_label.pack(anchor="w", pady=(4, 0))

# ---- Legend ----
legend_frame = tk.Frame(root, bg=COLOR_BG)
legend_frame.pack(fill="x", padx=30, pady=(14, 0))

you_legend = tk.Label(
    legend_frame, text="●  You play X", font=(FONT_FAMILY, 9, "bold"),
    bg=COLOR_BG, fg=COLOR_X
)
you_legend.pack(side="left")

ai_legend = tk.Label(
    legend_frame, text="●  AI plays O", font=(FONT_FAMILY, 9, "bold"),
    bg=COLOR_BG, fg=COLOR_O
)
ai_legend.pack(side="right")

# ---- Status line ----
status_label = tk.Label(
    root, text="Your move — tap a cell.",
    font=(FONT_FAMILY, 10, "italic"),
    bg=COLOR_BG, fg=COLOR_X, anchor="w"
)
status_label.pack(fill="x", padx=32, pady=(10, 4))

# ---- Board panel ----
board_card = tk.Frame(root, bg=COLOR_PANEL, highlightthickness=1,
                       highlightbackground=COLOR_BORDER)
board_card.pack(padx=30, pady=10)

board_inner = tk.Frame(board_card, bg=COLOR_PANEL)
board_inner.pack(padx=16, pady=16)

buttons = []

for row in range(3):
    for col in range(3):
        index = row * 3 + col

        btn = tk.Button(
            board_inner,
            text="",
            font=(FONT_FAMILY, 28, "bold"),
            width=4,
            height=2,
            bg=COLOR_CELL,
            fg=COLOR_TEXT,
            activebackground=COLOR_CELL_HOV,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda idx=index: player_move(idx)
        )

        btn.grid(row=row, column=col, padx=4, pady=4)
        btn.bind("<Enter>", lambda e, i=index: on_cell_enter(e, i))
        btn.bind("<Leave>", lambda e, i=index: on_cell_leave(e, i))

        buttons.append(btn)

# ---- Scoreboard ----
score_card = tk.Frame(root, bg=COLOR_PANEL, highlightthickness=1,
                       highlightbackground=COLOR_BORDER)
score_card.pack(fill="x", padx=30, pady=(14, 0))

score_label = tk.Label(
    score_card, text="You  0      AI  0      Draws  0",
    font=(FONT_FAMILY, 11, "bold"),
    bg=COLOR_PANEL, fg=COLOR_TEXT
)
score_label.pack(pady=12)

# ---- Restart button ----
reset_btn = tk.Button(root, text="↺  Restart Game", command=reset_game)
style_button(reset_btn, COLOR_O, "#ff4d5e")
reset_btn.pack(fill="x", padx=30, pady=20, ipady=4)

# ---- Footer ----
footer = tk.Label(
    root, text="Built with Python · Tkinter · Minimax Algorithm",
    font=(FONT_FAMILY, 8), bg=COLOR_BG, fg=COLOR_BORDER
)
footer.pack(pady=(0, 14))

root.mainloop()