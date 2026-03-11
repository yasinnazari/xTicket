from tkinter import *

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 40
SLOWNESS = 300
SNAKE_COLOR = "black"
BG_COLOR = "yellow"
FOOD_COLOR = "red"
direction="down"


def center_window(window):
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()

   w = (screen_width // 2 - window_width // 2) 
   h = (screen_height // 2 - window_height // 2)

   window.geometry(f"{window_width}x{window_height}+{w}+{h}")


def screen_base_configs(window, score):
   window.title('X SNAKE')
   window.resizable(False, False)

   label = Label(window, text=f"SCORE: {score}", font=('Letha', 25))
   label.pack()

   canvas = Canvas(window, bg=BG_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
   canvas.pack()

   label = Label(window, text=f" ", font=(5))
   label.pack()

   restart = Button(window, text="BOOM", fg="red", padx=5, pady=10, font=('bold'))
   restart.pack()

   label = Label(window, text=f" ", font=(5))
   label.pack()
