from tkinter import *
from snake_tools import center_window, screen_base_configs

score=0
BODY_SIZE = 3

def restart_game():
   global score
   score = 0

restart_game()
window = Tk()

screen_base_configs(window, score)

window.update()
center_window(window)
window.mainloop()
