import tkinter as tk
from tkinter import messagebox, font
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# COLOR PALETTE (Dark theme)
# =========================================================
COLOR_BG          = "#0f1117"   # app background
COLOR_PANEL       = "#171a23"   # cards / panels
COLOR_PANEL_ALT   = "#1d2129"   # input fields
COLOR_ACCENT      = "#e63946"   # primary accent (movie-ticket red)
COLOR_ACCENT_HOV  = "#ff4d5e"   # accent hover
COLOR_ACCENT_2    = "#3da9fc"   # secondary accent (links / highlights)
COLOR_TEXT        = "#f1f1f4"   # primary text
COLOR_TEXT_DIM    = "#9098a8"   # secondary text
COLOR_BORDER      = "#272b36"   # subtle borders
COLOR_SUCCESS     = "#4ade80"

FONT_FAMILY = "Segoe UI"


# -----------------------------
# Load Dataset Safely
# -----------------------------
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "movies.csv")

    movies = pd.read_csv(csv_path)

    cv = CountVectorizer()
    matrix = cv.fit_transform(movies["genre"])

    similarity = cosine_similarity(matrix)

except Exception as e:
    print("Error loading dataset:")
    print(e)
    exit()


# =========================================================
# RECOMMENDATION LOGIC (unchanged behaviour)
# =========================================================
def get_recommendations(movie_name):
    """Returns (status, payload).
    status: 'empty' | 'not_found' | 'ok'
    payload: list of all movie names (not_found) OR (title, [recs]) for ok
    """
    movie_name = movie_name.strip().lower()

    if movie_name == "":
        return "empty", None

    movie_indices = movies[movies["movie"].str.lower() == movie_name].index

    if len(movie_indices) == 0:
        return "not_found", list(movies["movie"])

    movie_index = movie_indices[0]
    distances = list(enumerate(similarity[movie_index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)

    recs = []
    for idx, score in sorted_movies:
        if idx != movie_index:
            recs.append((movies.iloc[idx]["movie"], score))
            if len(recs) == 5:
                break

    return "ok", (movies.iloc[movie_index]["movie"], recs)


# =========================================================
# UI ACTIONS
# =========================================================
def clear_placeholder(event=None):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg=COLOR_TEXT)


def restore_placeholder(event=None):
    if entry.get().strip() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg=COLOR_TEXT_DIM)


def set_status(text, color=COLOR_TEXT_DIM):
    status_label.config(text=text, fg=color)


def render_card(parent, rank, title, score=None):
    """A single recommendation row styled like a small card."""
    card = tk.Frame(parent, bg=COLOR_PANEL_ALT, highlightthickness=1,
                     highlightbackground=COLOR_BORDER)
    card.pack(fill="x", pady=4, padx=2)

    inner = tk.Frame(card, bg=COLOR_PANEL_ALT)
    inner.pack(fill="x", padx=12, pady=10)

    rank_badge = tk.Label(
        inner, text=f"{rank}", font=(FONT_FAMILY, 11, "bold"),
        bg=COLOR_ACCENT, fg="white", width=2, height=1
    )
    rank_badge.pack(side="left", padx=(0, 12))

    name_label = tk.Label(
        inner, text=title, font=(FONT_FAMILY, 11),
        bg=COLOR_PANEL_ALT, fg=COLOR_TEXT, anchor="w", justify="left"
    )
    name_label.pack(side="left", fill="x", expand=True)

    if score is not None:
        match_pct = f"{score * 100:.0f}% match"
        match_label = tk.Label(
            inner, text=match_pct, font=(FONT_FAMILY, 9, "bold"),
            bg=COLOR_PANEL_ALT, fg=COLOR_ACCENT_2
        )
        match_label.pack(side="right")


def clear_results_frame():
    for widget in results_container.winfo_children():
        widget.destroy()


def recommend_movies():
    clear_results_frame()

    typed = entry.get()
    if typed == placeholder_text:
        typed = ""

    status, payload = get_recommendations(typed)

    if status == "empty":
        messagebox.showwarning("Input Required", "Please enter a movie name.")
        set_status("Waiting for input…")
        return

    if status == "not_found":
        set_status("Movie not found — showing full catalog below.", COLOR_ACCENT)

        header = tk.Label(
            results_container,
            text="✗ Movie not found in database",
            font=(FONT_FAMILY, 12, "bold"),
            bg=COLOR_BG, fg=COLOR_ACCENT, anchor="w"
        )
        header.pack(fill="x", pady=(0, 10))

        sub = tk.Label(
            results_container,
            text="Available movies:",
            font=(FONT_FAMILY, 10),
            bg=COLOR_BG, fg=COLOR_TEXT_DIM, anchor="w"
        )
        sub.pack(fill="x", pady=(0, 8))

        for movie in payload:
            row = tk.Label(
                results_container, text=f"•  {movie}",
                font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_TEXT,
                anchor="w"
            )
            row.pack(fill="x", pady=1)
        return

    # status == "ok"
    title, recs = payload
    set_status(f"Showing {len(recs)} recommendations for \"{title}\"", COLOR_SUCCESS)

    header = tk.Label(
        results_container,
        text=f"🎬 Because you liked \"{title}\"",
        font=(FONT_FAMILY, 13, "bold"),
        bg=COLOR_BG, fg=COLOR_TEXT, anchor="w", wraplength=480, justify="left"
    )
    header.pack(fill="x", pady=(0, 12))

    for i, (name, score) in enumerate(recs, start=1):
        render_card(results_container, i, name, score)


def clear_results():
    entry.delete(0, tk.END)
    restore_placeholder()
    clear_results_frame()
    set_status("Waiting for input…")
    show_welcome()


def show_welcome():
    clear_results_frame()
    welcome = tk.Label(
        results_container,
        text="Try one of these to get started:",
        font=(FONT_FAMILY, 11, "bold"),
        bg=COLOR_BG, fg=COLOR_TEXT, anchor="w"
    )
    welcome.pack(fill="x", pady=(4, 10))

    sample_titles = list(movies["movie"].head(5))
    for t in sample_titles:
        chip = tk.Label(
            results_container, text=f"🎞  {t}",
            font=(FONT_FAMILY, 10), bg=COLOR_PANEL_ALT, fg=COLOR_TEXT_DIM,
            anchor="w", padx=10, pady=6
        )
        chip.pack(fill="x", pady=3)

        def make_handler(title=t):
            def handler(event):
                entry.delete(0, tk.END)
                entry.insert(0, title)
                entry.config(fg=COLOR_TEXT)
                recommend_movies()
            return handler

        chip.bind("<Button-1>", make_handler())
        chip.bind("<Enter>", lambda e, w=chip: w.config(bg=COLOR_BORDER))
        chip.bind("<Leave>", lambda e, w=chip: w.config(bg=COLOR_PANEL_ALT))


def on_enter_key(event):
    recommend_movies()


# =========================================================
# GUI BUILD
# =========================================================
root = tk.Tk()
root.title("CineMatch — Movie Recommendation System")
root.geometry("620x680")
root.configure(bg=COLOR_BG)
root.resizable(False, False)

# ---- Header ----
header_frame = tk.Frame(root, bg=COLOR_BG)
header_frame.pack(fill="x", padx=30, pady=(28, 0))

title_label = tk.Label(
    header_frame,
    text="🎬 CineMatch",
    font=(FONT_FAMILY, 24, "bold"),
    bg=COLOR_BG, fg=COLOR_TEXT
)
title_label.pack(anchor="w")

subtitle_label = tk.Label(
    header_frame,
    text="Find your next favourite movie, based on what you already love.",
    font=(FONT_FAMILY, 10),
    bg=COLOR_BG, fg=COLOR_TEXT_DIM
)
subtitle_label.pack(anchor="w", pady=(4, 0))

# ---- Search bar card ----
search_card = tk.Frame(root, bg=COLOR_PANEL, highlightthickness=1,
                        highlightbackground=COLOR_BORDER)
search_card.pack(fill="x", padx=30, pady=20)

search_inner = tk.Frame(search_card, bg=COLOR_PANEL)
search_inner.pack(fill="x", padx=18, pady=16)

placeholder_text = "e.g. Inception, Titanic, Avatar…"

entry = tk.Entry(
    search_inner,
    font=(FONT_FAMILY, 12),
    bg=COLOR_PANEL_ALT,
    fg=COLOR_TEXT_DIM,
    insertbackground=COLOR_TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=COLOR_BORDER,
    highlightcolor=COLOR_ACCENT_2,
)
entry.pack(fill="x", ipady=8, ipadx=8)
entry.insert(0, placeholder_text)
entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<FocusOut>", restore_placeholder)
entry.bind("<Return>", on_enter_key)

btn_row = tk.Frame(search_inner, bg=COLOR_PANEL)
btn_row.pack(fill="x", pady=(14, 0))


def style_button(btn, bg, hover_bg, fg="white"):
    btn.config(
        bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
        relief="flat", bd=0, font=(FONT_FAMILY, 11, "bold"),
        cursor="hand2", padx=14, pady=8
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))


recommend_btn = tk.Button(btn_row, text="🔍  Recommend", command=recommend_movies)
style_button(recommend_btn, COLOR_ACCENT, COLOR_ACCENT_HOV)
recommend_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

clear_btn = tk.Button(btn_row, text="✕  Clear", command=clear_results)
style_button(clear_btn, COLOR_PANEL_ALT, COLOR_BORDER, fg=COLOR_TEXT)
clear_btn.pack(side="left", expand=True, fill="x", padx=(8, 0))

# ---- Status line ----
status_label = tk.Label(
    root, text="Waiting for input…",
    font=(FONT_FAMILY, 9, "italic"),
    bg=COLOR_BG, fg=COLOR_TEXT_DIM, anchor="w"
)
status_label.pack(fill="x", padx=32, pady=(0, 6))

# ---- Results area (scrollable) ----
results_outer = tk.Frame(root, bg=COLOR_BG)
results_outer.pack(fill="both", expand=True, padx=30, pady=(0, 20))

canvas = tk.Canvas(results_outer, bg=COLOR_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(results_outer, orient="vertical", command=canvas.yview)
results_container = tk.Frame(canvas, bg=COLOR_BG)

results_container.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=results_container, anchor="nw", width=540)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", on_mousewheel)

# ---- Footer ----
footer = tk.Label(
    root, text="Built with Python · Tkinter · scikit-learn",
    font=(FONT_FAMILY, 8), bg=COLOR_BG, fg=COLOR_BORDER
)
footer.pack(pady=(0, 12))

show_welcome()

root.mainloop()