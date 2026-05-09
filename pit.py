import tkinter as tk
import random

#window setup
root = tk.Tk()
root.title("GUESS THE WORD")
root.geometry("770x660")
root.configure(bg="#0D0D0D")

#colors
BG        = "#0D0D0D"
PANEL     = "#161616"
BORDER    = "#2A2A2A"
GREEN     = "#39FF14"   
RED       = "#FF3131"   
YELLOW    = "#FFD600"   
WHITE     = "#F0F0F0"
GRAY      = "#444444"
BTN_DARK  = "#1E1E1E"

#choices of words by category
WORD_BANK = {
    "Technology": [
        "PYTHON", "ALGORITHM", "KEYBOARD", "MONITOR", "NETWORK",
        "COMPILER", "DATABASE", "INTERFACE", "PROCESSOR", "PROGRAMMING",
        "PROTOCOL", "BANDWIDTH", "RECURSION", "VARIABLE", "FUNCTION",
    ],
    "Science": [
        "GALAXY", "NEUTRON", "ELECTRON", "MOLECULE", "NUCLEUS",
        "PHOTON", "PROTON", "GRAVITY", "ENTROPY", "PLASMA",
        "QUANTUM", "ISOTOPE", "CATALYST", "OSMOSIS", "CHROMOSOME",
    ],
    "Animals": [
        "ELEPHANT", "PENGUIN", "CROCODILE", "OCTOPUS", "CHEETAH",
        "DOLPHIN", "GORILLA", "HAMSTER", "JAGUAR", "KANGAROO",
        "LEOPARD", "MONGOOSE", "CAPYBARA", "MONKEY", "SALAMANDER",
    ],
    "Geography": [
        "ANTARCTICA", "HIMALAYA", "SAHARA", "AMAZON", "PACIFIC",
        "EQUATOR", "VOLCANO", "GLACIER", "PENINSULA", "ARCHIPELAGO",
        "MERIDIAN", "PLATEAU", "CANYON", "TUNDRA", "SAVANNA",
    ],
}

#random picks
ALL_WORDS = [w for words in WORD_BANK.values() for w in words]

# ---------------- GAME STATE ---------------- #
chosen_word     = ""
chosen_category = ""
guessed_letters = []
wrong_guesses   = 0
max_wrong       = 6
game_over       = False
letter_buttons  = {}

# Widget refs that need to be global
grid_frame      = None
keyboard_frame  = None
hangman_canvas  = None
result_label    = None
tries_label     = None
category_label  = None

# ---------------- HELPERS ---------------- #

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def pick_word(category=None):
    global chosen_word, chosen_category
    if category and category in WORD_BANK:
        chosen_word = random.choice(WORD_BANK[category])
        chosen_category = category
    else:
        chosen_category, words = random.choice(list(WORD_BANK.items()))
        chosen_word = random.choice(words)
    return chosen_word, chosen_category

#draw hangman
def draw_hangman(canvas, wrong):
    canvas.delete("all")
    W, H = 280, 300

    scaffold = "#555555"
    sw = 3
    canvas.create_line(20, H-10, W-20, H-10, fill=scaffold, width=sw+1)
    canvas.create_line(60, H-10, 60, 20, fill=scaffold, width=sw)
    canvas.create_line(60, 20, 190, 20, fill=scaffold, width=sw)
    canvas.create_line(190, 20, 190, 60, fill=scaffold, width=sw)

    body_color = WHITE if wrong < max_wrong else RED

    if wrong >= 1:
        canvas.create_oval(165, 60, 215, 110, outline=body_color, width=3)
        if wrong >= 6:
            canvas.create_text(183, 80, text="×", fill=RED, font=("Courier", 11, "bold"))
            canvas.create_text(197, 80, text="×", fill=RED, font=("Courier", 11, "bold"))
            canvas.create_text(190, 97, text="‿", fill=RED, font=("Courier", 13))
        else:
            canvas.create_oval(178, 77, 184, 83, fill=body_color, outline=body_color)
            canvas.create_oval(196, 77, 202, 83, fill=body_color, outline=body_color)
            canvas.create_arc(180, 88, 200, 102, start=200, extent=-160, outline=body_color, width=2)

    if wrong >= 2:
        canvas.create_line(190, 110, 190, 185, fill=body_color, width=3)
    if wrong >= 3:
        canvas.create_line(190, 130, 155, 160, fill=body_color, width=3)
    if wrong >= 4:
        canvas.create_line(190, 130, 225, 160, fill=body_color, width=3)
    if wrong >= 5:
        canvas.create_line(190, 185, 158, 225, fill=body_color, width=3)
    if wrong >= 6:
        canvas.create_line(190, 185, 222, 225, fill=body_color, width=3)

#word grid
def update_word_grid():
    global grid_frame
    for widget in grid_frame.winfo_children():
        widget.destroy()

    all_correct = all(l in guessed_letters for l in chosen_word)

    for letter in chosen_word:
        revealed = letter in guessed_letters
        display  = letter if revealed else ""

        box = tk.Label(
            grid_frame,
            text=display,
            font=("Fixedsys", 18, "bold"),
            width=2, height=1,
            fg=GREEN if (revealed and all_correct) else WHITE,
            bg=PANEL, relief="flat", bd=0, padx=4,
        )
        box.pack(side="left", padx=5)

        line = tk.Frame(grid_frame, bg=GREEN if revealed else BORDER, height=2, width=38)
        line.place(in_=box, relx=0, rely=1.0, anchor="nw", x=4, y=-4)

#check game
def check_game():
    global game_over

    if all(l in guessed_letters for l in chosen_word):
        result_label.config(text="✓  YOU WIN!", fg=GREEN)
        game_over = True
        disable_keyboard()

    elif wrong_guesses >= max_wrong:
        result_label.config(text=f"✗  GAME OVER — {chosen_word}", fg=RED)
        game_over = True
        disable_keyboard()
        for letter in chosen_word:
            if letter not in guessed_letters:
                guessed_letters.append(letter)
        update_word_grid()

#keyboard
def disable_keyboard():
    for btn in letter_buttons.values():
        btn.config(state="disabled")

def letter_click(letter):
    global wrong_guesses

    if game_over or letter in guessed_letters:
        return

    guessed_letters.append(letter)

    if letter in chosen_word:
        letter_buttons[letter].config(bg=GREEN, fg="#000000", state="disabled")
    else:
        wrong_guesses += 1
        letter_buttons[letter].config(bg=RED, fg=WHITE, state="disabled")

    draw_hangman(hangman_canvas, wrong_guesses)
    update_word_grid()
    tries_label.config(text=f"LIVES  {max_wrong - wrong_guesses} / {max_wrong}")
    check_game()

#physical keyboard input
def on_key_press(event):
    letter = event.char.upper()
    if letter in letter_buttons:
        letter_click(letter)

#restart game
def restart_game(same_category=False):
    global chosen_word, chosen_category, guessed_letters
    global wrong_guesses, game_over, letter_buttons

    cat = chosen_category if same_category else None
    pick_word(cat)

    guessed_letters = []
    wrong_guesses   = 0
    game_over       = False

    result_label.config(text="")
    tries_label.config(text=f"LIVES  {max_wrong} / {max_wrong}")
    category_label.config(text=f"Category: {chosen_category}", fg=YELLOW)

    draw_hangman(hangman_canvas, 0)
    update_word_grid()

    for btn in letter_buttons.values():
        btn.config(state="normal", bg=BTN_DARK, fg=WHITE)

#main menu
def show_main_menu():
    clear_screen()

    canvas_bg = tk.Canvas(root, width=800, height=700, bg=BG, highlightthickness=0)
    canvas_bg.place(x=0, y=0)
    for row in range(0, 700, 28):
        for col in range(0, 800, 28):
            canvas_bg.create_oval(col, row, col+2, row+2, fill="#1E1E1E", outline="")

    tk.Label(root, text="GUESS THE WORD",
             font=("Fixedsys", 52, "bold"),
             fg=GREEN, bg=BG).place(relx=0.5, y=130, anchor="center")

    tk.Label(root, text="guess the word before the man is hanged",
             font=("Fixedsys", 13), fg="#878585", bg=BG).place(relx=0.5, y=190, anchor="center")

    mini = tk.Canvas(root, width=250, height=180, bg=BG, highlightthickness=0)
    mini.place(relx=0.5, y=290, anchor="center")
    draw_hangman(mini, 4)

    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.place(relx=0.5, y=460, anchor="center")

    def styled_btn(parent, text, color, cmd, width=18):
        return tk.Button(
            parent, text=text,
            font=("Fixedsys", 15, "bold"),
            width=width, height=1,
            bg=color, fg="#000000" if color in (GREEN, YELLOW) else WHITE,
            activebackground=color,
            relief="flat", bd=0, cursor="hand2",
            command=cmd,
        )

    styled_btn(btn_frame, "▶  START", GREEN, lambda: show_category_menu()).pack(pady=7)
    styled_btn(btn_frame, "RANDOM WORD", YELLOW, lambda: (pick_word(), show_game_screen())).pack(pady=7)
    styled_btn(btn_frame, "✕  QUIT", "#333333", root.quit, width=18).pack(pady=7)

    tk.Label(root, text="← select a category or start randomly →",
             font=("Courier", 10), fg="#878585", bg=BG).place(relx=0.5, y=550, anchor="center")

#category menu
def show_category_menu():
    clear_screen()

    tk.Label(root, text="CHOOSE A CATEGORY",
             font=("Fixedsys", 30, "bold"),
             fg=WHITE, bg=BG).place(relx=0.5, y=147, anchor="center")

    tk.Label(root, text="pick a topic or go random",
             font=("Courier", 12), fg="#878585", bg=BG).place(relx=0.5, y=190, anchor="center")

    cat_frame = tk.Frame(root, bg=BG)
    cat_frame.place(relx=0.5, y=340, anchor="center")

    colors = [GREEN, "#00BFFF", YELLOW, "#FF69B4"]
    icons  = ["⌨", "🔬", "🐾", "🌍"]

    for i, (cat, clr, icon) in enumerate(zip(WORD_BANK.keys(), colors, icons)):
        row = i // 2
        col = i % 2

        btn = tk.Button(
            cat_frame,
            text=f"{icon}  {cat}",
            font=("Courier", 16, "bold"),
            width=20, height=3,
            bg=PANEL, fg=clr,
            activebackground=BORDER,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=clr,
            cursor="hand2",
            command=lambda c=cat: (pick_word(c), show_game_screen()),
        )
        btn.grid(row=row, column=col, padx=12, pady=12)

    tk.Button(root, text="← BACK",
              font=("Courier", 13, "bold"),
              bg=BG, fg="#878585",
              activebackground=BG, activeforeground=WHITE,
              relief="flat", bd=0, cursor="hand2",
              command=show_main_menu).place(relx=0.5, y=490, anchor="center")

#game screen
def show_game_screen():
    clear_screen()

    global grid_frame, keyboard_frame, hangman_canvas
    global result_label, tries_label, category_label
    global letter_buttons
    letter_buttons = {}

    # ── Header bar ──
    header = tk.Frame(root, bg=PANEL, height=54)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="GUESS THE WORD",
             font=("Fixedsys", 18, "bold"),
             fg=GREEN, bg=PANEL).place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(header, text="← MENU",
              font=("Courier", 11, "bold"),
              bg=PANEL, fg="#878585",
              activebackground=PANEL, activeforeground=WHITE,
              relief="flat", bd=0, cursor="hand2",
              command=show_main_menu).place(x=18, rely=0.5, anchor="w")

    #category label
    category_label = tk.Label(
        root,
        text=f"Category: {chosen_category}",
        font=("Courier", 12, "bold"),
        fg=YELLOW, bg=BG)
    category_label.pack(pady=(10, 0))

    #tries
    tries_label = tk.Label(
        root,
        text=f"LIVES  {max_wrong} / {max_wrong}",
        font=("Courier", 14, "bold"),
        fg=WHITE, bg=BG)
    tries_label.pack()

    # ── Top row: wrong guesses left | hangman center | spacer right ──
    top_row = tk.Frame(root, bg=BG)
    top_row.pack(fill="x", padx=20, pady=(4, 0))

    wrong_label_var = tk.StringVar(value="—")
    wrong_col = tk.Frame(top_row, bg=BG, width=200)
    wrong_col.pack(side="left", anchor="n")
    wrong_col.pack_propagate(False)
    tk.Label(wrong_col, text="WRONG GUESSES",
             font=("Courier", 5), fg=GRAY, bg=BG).pack(pady=(8, 2))
    tk.Label(wrong_col, textvariable=wrong_label_var,
             font=("Courier", 13, "bold"),
             fg=RED, bg=BG, wraplength=190, justify="center").pack()

    # Hangman canvas — center
    hangman_canvas = tk.Canvas(
        top_row, width=230, height=230,
        bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
    hangman_canvas.pack(side="left", expand=True)
    draw_hangman(hangman_canvas, 0)

    # Spacer right to balance wrong guesses column
    tk.Frame(top_row, bg=BG, width=200).pack(side="left")

    # ── Word grid — centered, above keyboard ──
    tk.Label(root, text="GUESS THE WORD",
             font=("Courier", 11, "bold"),
             fg=GRAY, bg=BG).pack(pady=(8, 4))

    grid_frame = tk.Frame(root, bg=BG)
    grid_frame.pack()
    update_word_grid()

    # Result
    result_label = tk.Label(root, text="",
                             font=("Courier", 14, "bold"), bg=BG)
    result_label.pack(pady=(5, 0))

    # ── Keyboard — centered below word grid ──
    def patched_click(letter):
        letter_click(letter)
        wrongs = [l for l in guessed_letters if l not in chosen_word]
        wrong_label_var.set("  ".join(wrongs) if wrongs else "—")

    keyboard_frame = tk.Frame(root, bg=BG)
    keyboard_frame.pack(pady=(0, 4))
    create_keyboard_patched(keyboard_frame, patched_click)

    #bottom buttons
    bottom = tk.Frame(root, bg=BG)
    bottom.pack(pady=20)

    tk.Button(bottom, text="NEW WORD",
              font=("Courier", 12, "bold"),
              width=14, height=1,
              bg=PANEL, fg=GREEN,
              activebackground=BORDER,
              relief="flat", bd=0,
              highlightthickness=1, highlightbackground=GREEN,
              cursor="hand2",
              command=lambda: restart_game(False)).grid(row=0, column=0, padx=6)

    tk.Button(bottom, text="SAME CATEGORY",
              font=("Courier", 12, "bold"),
              width=14, height=1,
              bg=PANEL, fg=YELLOW,
              activebackground=BORDER,
              relief="flat", bd=0,
              highlightthickness=1, highlightbackground=YELLOW,
              cursor="hand2",
              command=lambda: restart_game(True)).grid(row=0, column=1, padx=6)

    tk.Button(bottom, text="HINT",
              font=("Courier", 12, "bold"),
              width=14, height=1,
              bg=PANEL, fg="#00BFFF",
              activebackground=BORDER,
              relief="flat", bd=0,
              highlightthickness=1, highlightbackground="#00BFFF",
              cursor="hand2",
              command=lambda: use_hint(wrong_label_var)).grid(row=0, column=2, padx=6)

    tk.Button(bottom, text="EXIT",
              font=("Courier", 12, "bold"),
              width=14, height=1,
              bg=PANEL, fg=WHITE,
              activebackground=BORDER,
              relief="flat", bd=0,
              highlightthickness=1, highlightbackground=GRAY,
              cursor="hand2",
              command=root.quit).grid(row=0, column=3, padx=6)

    #physical keyboard
    root.bind("<Key>", on_key_press)
    root.focus_set()

def create_keyboard_patched(parent, click_fn):
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    for row in rows:
        rf = tk.Frame(parent, bg=BG)
        rf.pack(pady=3)
        for letter in row:
            btn = tk.Button(
                rf, text=letter,
                font=("Courier", 14, "bold"),
                width=4, height=1,
                bg=BTN_DARK, fg=WHITE,
                activebackground=GRAY, activeforeground=WHITE,
                relief="flat", bd=0,
                highlightthickness=1, highlightbackground=BORDER,
                cursor="hand2",
                command=lambda l=letter: click_fn(1),
            )
            btn.pack(side="left", padx=2)
            letter_buttons[letter] = btn


#hint system
_hints_used = 0
MAX_HINTS   = 3

def use_hint(wrong_label_var):
    global wrong_guesses, _hints_used

    if game_over:
        return

    if _hints_used >= MAX_HINTS:
        result_label.config(text=f"No hints left! (max {MAX_HINTS})", fg=YELLOW)
        return

    remaining = [l for l in chosen_word if l not in guessed_letters]
    if not remaining:
        return

    hint_letter = random.choice(list(set(remaining)))
    guessed_letters.append(hint_letter)
    letter_buttons[hint_letter].config(bg="#1A4A1A", fg=GREEN, state="disabled")

    wrong_guesses += 1
    _hints_used   += 1

    wrongs = [l for l in guessed_letters if l not in chosen_word]
    wrong_label_var.set("  ".join(wrongs) if wrongs else "—")

    draw_hangman(hangman_canvas, wrong_guesses)
    update_word_grid()
    tries_label.config(text=f"LIVES  {max_wrong - wrong_guesses} / {max_wrong}")
    check_game()

_original_restart = restart_game

def restart_game(same_category=False):
    global _hints_used
    _hints_used = 0
    _original_restart(same_category)

#launch
pick_word()
show_main_menu()
root.mainloop()