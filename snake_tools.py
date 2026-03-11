from tkinter import *

def center_window(window):
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()
   x = (screen_width - window_width) // 2 
   y = (screen_height - window_height) // 2
   window.geometry(f"{window_width}x{window_height}+{x}+{y}")
