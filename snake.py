from tkinter import *
from snake_tools import center_window, screen_base_configs

score=0
SNAKE_COLOR = "black"
FOOD_COLOR = "red"
SPACE_SIZE = 40
BODY_SIZE = 3

class Snake:
   def __init__(self):
      self.body_size = BODY_SIZE
      self.coordinates = [[0, 0] for _ in range(0, BODY_SIZE)]
      self.squares = []

      for x, y in self.coordinates:
         square = Canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
         self.squares.append(square)

def restart_game():
   score = 0

window = Tk()
screen_base_configs(window, score)

window.update()
center_window(window)
window.mainloop()
