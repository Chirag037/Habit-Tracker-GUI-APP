import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

DATA_FILE = "habits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_habit():
    name = entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a habit name.")
        return

    data = load_data()
    if name in data:
        messagebox.showinfo("Exists", f"Habit '{name}' already exists.")
    else:
        data[name] = {"dates": [], "streak": 0}
        save_data(data)
        entry.delete(0, tk.END)
        refresh_ui()

def mark_done(habit, var):
    today = datetime.today().strftime("%Y-%m-%d")
    data = load_data()

    if today not in data[habit]["dates"]:
        data[habit]["dates"].append(today)
        data[habit]["streak"] += 1
        save_data(data)
    refresh_ui()

def refresh_ui():
    for widget in habits_frame.winfo_children():
        widget.destroy()

    data = load_data()
    today = datetime.today().strftime("%Y-%m-%d")

    for habit in data:
        is_done = today in data[habit]["dates"]
        var = tk.BooleanVar(value=is_done)
        check = tk.Checkbutton(habits_frame, text=f"{habit} (Streak: {data[habit]['streak']})",
                               variable=var, command=lambda h=habit, v=var: mark_done(h, v))
        if is_done:
            check.config(state=tk.DISABLED)
        check.pack(anchor="w", pady=2)

# GUI setup
root = tk.Tk()
root.title("Habit Tracker")
root.geometry("400x500")
root.resizable(False, False)

title = tk.Label(root, text="Habit Tracker", font=("Helvetica", 18))
title.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

add_button = tk.Button(root, text="Add Habit", command=add_habit)
add_button.pack(pady=5)

separator = tk.Label(root, text="----------------------------")
separator.pack()

habits_frame = tk.Frame(root)
habits_frame.pack(pady=10, fill="both", expand=True)

refresh_ui()

root.mainloop()
