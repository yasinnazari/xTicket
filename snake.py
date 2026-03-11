from tkinter import *
from snake_tools import center_window
# ------------------------
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPACE_SIZE = 40
SLOWNESS = 300
SNAKE_COLOR = "black"
BG_COLOR = "yellow"
FOOD_COLOR = "red"

score=0
direction="down"
# window_height = 

# --------------------------

window = Tk()
window.title('X SNAKE')
window.resizable(False, False)

label = Label(window, text=f"SCORE: {score}", font=('Letha', 25))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

label = Label(window, text=f" ", font=('Letha', 5))
label.pack()

restart = Button(window, text="BOOM", fg="red", padx=5, pady=10, font=('bold'))
restart.pack()

label = Label(window, text=f" ", font=('Letha', 5))
label.pack()

window.update()
center_window(window)
window.mainloop()
