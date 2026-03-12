from tkinter import *

direction="down"

def center_window(window):
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()

   w = (screen_width // 2 - window_width // 2) 
   h = (screen_height // 2 - window_height // 2)

   window.geometry(f"{window_width}x{window_height}+{w}+{h}")


def restart_game():
   score = 0
