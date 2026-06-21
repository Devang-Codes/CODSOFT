import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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


# -----------------------------
# Recommendation Function
# -----------------------------
def recommend_movies():

    movie_name = entry.get().strip().lower()

    result_box.delete(1.0, tk.END)

    if movie_name == "":
        messagebox.showwarning(
            "Input Required",
            "Please enter a movie name."
        )
        return

    movie_indices = movies[
        movies["movie"].str.lower() == movie_name
    ].index

    if len(movie_indices) == 0:

        result_box.insert(
            tk.END,
            "Movie not found in database.\n\n"
        )

        result_box.insert(
            tk.END,
            "Available Movies:\n\n"
        )

        for movie in movies["movie"]:
            result_box.insert(
                tk.END,
                movie + "\n"
            )

        return

    movie_index = movie_indices[0]

    distances = list(
        enumerate(similarity[movie_index])
    )

    sorted_movies = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    result_box.insert(
        tk.END,
        f"Recommendations for:\n{movies.iloc[movie_index]['movie']}\n\n"
    )

    count = 0

    for movie in sorted_movies:

        if movie[0] != movie_index:

            result_box.insert(
                tk.END,
                f"• {movies.iloc[movie[0]]['movie']}\n"
            )

            count += 1

            if count == 5:
                break


# -----------------------------
# Clear Function
# -----------------------------
def clear_results():
    entry.delete(0, tk.END)
    result_box.delete(1.0, tk.END)


# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("600x500")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🎬 Movie Recommendation System",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Enter a movie name to get recommendations",
    font=("Arial", 10)
)
subtitle.pack()

entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12)
)
entry.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

recommend_btn = tk.Button(
    btn_frame,
    text="Recommend",
    width=15,
    command=recommend_movies
)
recommend_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    width=15,
    command=clear_results
)
clear_btn.grid(row=0, column=1, padx=10)

result_box = tk.Text(
    root,
    width=60,
    height=18,
    font=("Arial", 11)
)
result_box.pack(pady=20)

result_box.insert(
    tk.END,
    "Try:\n\n"
    "Avatar\n"
    "Iron Man\n"
    "Inception\n"
    "Interstellar\n"
    "Titanic\n"
)
root.mainloop()