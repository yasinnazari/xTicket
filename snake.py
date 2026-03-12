import random
from tkinter import *
from snake_tools import center_window, restart_game

score=0
SNAKE_COLOR = "#6a00ff"
FOOD_COLOR = "red"
BG_COLOR = "darkgreen"
GAME_WIDTH = 600
GAME_HEIGHT = 600
SLOWNESS = 300
SPACE_SIZE = 30
BODY_SIZE = 3

class Snake:
   def __init__(self):
      self.body_size = BODY_SIZE
      self.coordinates = [[0, 0] for _ in range(0, BODY_SIZE)]
      self.squares = []

      for x, y in self.coordinates:
         square = canvas.create_rectangle(
            x, y,
            x+SPACE_SIZE, y+SPACE_SIZE,
            fill=SNAKE_COLOR,
            tag='snake',
         )

         self.squares.append(square)


class Food:
   def __init__(self):
      x = random.randint(0, GAME_WIDTH // SPACE_SIZE - 1) * SPACE_SIZE
      y = random.randint(0, GAME_HEIGHT // SPACE_SIZE - 1) * SPACE_SIZE

      self.coordinate = [x, y]

      canvas.create_rectangle(
         x, y,
         x+SPACE_SIZE, y+SPACE_SIZE,
         fill=FOOD_COLOR,
         tag='food'
      )

def next_turn(snake, food):
   x, y = snake.coordinates[0]
   print(x,y)
next_turn()

# Create game screen
window = Tk()
window.title('ETHNAKE')
window.resizable(False, False)

# Score Label
label = Label(window, text=f" ", font=(3))
label.pack()
label = Label(window, text=f"SCORE: {score}", font=('Letha', 25))
label.pack()
label = Label(window, text=f" ", font=(3))
label.pack()

# Main Boom
canvas = Canvas(window, bg=BG_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

# Reset Button
label = Label(window, text=f" ", font=(3))
label.pack()
restart = Button(window, text="BOOM", fg="red", padx=5, pady=10, font=('bold'))
restart.pack()
label = Label(window, text=f" ", font=(3))
label.pack()

window.update()

snake = Snake()
food = Food()

center_window(window)

window.mainloop()
