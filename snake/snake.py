import random
from tkinter import *
from snake_options import center_window

score=0
direction="down"
SNAKE_COLOR = "#6a00ff"
FOOD_COLOR = "red"
BG_COLOR = "darkgreen"
GAME_WIDTH = 600
GAME_HEIGHT = 600
SLOWNESS = 120
SPACE_SIZE = 20
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

   if direction == 'right':
      x += SPACE_SIZE
   elif direction == 'left':
      x -= SPACE_SIZE
   elif direction == 'up':
      y -= SPACE_SIZE
   elif direction == 'down':
      y += SPACE_SIZE

   snake.coordinates.insert(0, [x, y])
   new_sq = canvas.create_rectangle(
      x, y,
      x+SPACE_SIZE, y+SPACE_SIZE,
      fill=SNAKE_COLOR
   )
   snake.squares.insert(0, new_sq)

   if x == food.coordinate[0] and y == food.coordinate[1]:
      global score
      score += 1
      label.config(text=f"🏆 {score} ", font=('Georgia', 20))
      canvas.delete("food")
      food = Food()
   else:
      del snake.coordinates[-1]
      canvas.delete(snake.squares[-1])
      del snake.squares[-1]

   if check_game_over():
      game_over()
   else:
      window.after(SLOWNESS, next_turn, snake, food)

def check_game_over():
   pass

def game_over():
   pass


def restart_game():
   global score

   score += 0

def change_direction(dir):
   global direction

   if dir == 'left':
      if direction != 'right':
         direction = 'left'
   if dir == 'right':
      if direction != 'left':
         direction = 'right'
   if dir == 'up':
      if direction != 'down':
         direction = 'up'
   if dir == 'down':
      if direction != 'up':
         direction = 'down'


# Create Game Screen
window = Tk()
window.title('ETHNAKE')
window.resizable(False, False)

# Score Label
sp1 = Label(window, text=f" ", font=(2))
sp1.pack()
label = Label(window, text=f"🏆 {score} ", font=('Georgia', 20))
label.pack()
sp2 = Label(window, text=f" ", font=(2))
sp2.pack()

# Main Boom
canvas = Canvas(window, bg=BG_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

# Reset Button
sp3 = Label(window, text=f" ", font=(3))
sp3.pack()
restart = Button(window, text="BOOM", fg="red", padx=5, pady=10, font=('bold'), command=restart_game)
restart.pack()
sp4 = Label(window, text=f" ", font=(3))
sp4.pack()

window.update()

center_window(window)
window.bind('<Up>', lambda ev: change_direction("up"))
window.bind('<Down>', lambda ev: change_direction("down"))
window.bind('<Left>', lambda ev: change_direction("left"))
window.bind('<Right>', lambda ev: change_direction("right"))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
