import tkinter as tk

root = tk.Tk()
root.title("Guess the Word")
root.geometry("800x500") 
root.resizable(False, False)
fg="#1B1B1B"

title_label = tk.Label(
        root,
        text="GUESS THE WORD",
        font=("Fixedsys", 60, "bold"),
        fg="#0D0202",
    )
title_label.pack(pady=87)

    # Subtitle / Instruction
subtitle_label = tk.Label(
        root,
        text="Welcome! Click Start to play.",
        font=("Arial", 9)
    )
subtitle_label.pack(pady=10)

    # Start Button (no function yet)
start_button = tk.Button(
        root,
        text="Start Game",
        width=15,
        height=2
    )
start_button.pack(side="left", padx=190, pady=25)

    # Exit Button
exit_button = tk.Button(
        root,
        text="Exit",
        width=15,
        height=2,
        command=root.quit
    )
exit_button.pack(side="left", padx=10, pady=25)

root.mainloop()