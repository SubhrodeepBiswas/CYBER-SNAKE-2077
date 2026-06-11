
from turtle import Turtle, Screen
import random
import time

# ==========================
# CONSTANTS
# ==========================
SCREEN_SIZE = 700
MOVE_DISTANCE = 20
GAME_SPEED = 0.07

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]

BG_COLOR = "#080b12"        # Deep dark background
SNAKE_COLOR = "#00fff7"     # Neon cyan
FOOD_COLOR = "#ff00aa"      # Neon pink
TEXT_COLOR = "#00ff88"      # Neon green
BUTTON_BG = "#0d1b2a"
BUTTON_FG = "#00fff7"
BUTTON_ACTIVE = "#00fff7"

FONT = ("Arial", 20, "bold")
FONT_TITLE = ("Arial", 36, "bold")
FONT_SUBTITLE = ("Arial", 16, "normal")
FONT_SCORE_BIG = ("Arial", 28, "bold")


# ==========================
# SNAKE CLASS
# ==========================
class Snake:

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        segment = Turtle("square")
        segment.penup()
        segment.color(SNAKE_COLOR)
        segment.speed("fastest")
        segment.goto(position)
        self.segments.append(segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def reset(self):
        for seg in self.segments:
            seg.hideturtle()
            seg.goto(2000, 2000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


# ==========================
# FOOD CLASS
# ==========================
class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(0.7, 0.7)
        self.color(FOOD_COLOR)
        self.speed("fastest")
        self.hideturtle()

    def show(self):
        self.showturtle()
        self.refresh()

    def hide_food(self):
        self.hideturtle()
        self.goto(2000, 2000)

    def refresh(self):
        random_x = random.randint(-310, 310)
        random_y = random.randint(-310, 310)
        self.goto(random_x, random_y)


# ==========================
# SCOREBOARD CLASS
# ==========================
class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color(TEXT_COLOR)
        self.penup()
        self.hideturtle()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0

    def show_hud(self):
        self.clear()
        self.goto(-340, 310)
        self.write(f"Score: {self.score}", align="left", font=FONT)
        self.goto(340, 310)
        self.write(f"Best: {self.high_score}", align="right", font=FONT)

    def increase_score(self):
        self.score += 1
        self.show_hud()

    def clear_display(self):
        self.clear()


# ==========================
# OVERLAY TURTLE (for screens)
# ==========================
class Overlay(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color(TEXT_COLOR)

    def show_start_screen(self):
        self.clear()
        # Title
        self.color("#00fff7")
        self.goto(0, 130)
        self.write("CYBER SNAKE", align="center", font=("Arial", 44, "bold"))

        self.color("#ff00aa")
        self.goto(0, 80)
        self.write("2077", align="center", font=("Arial", 28, "bold"))

        self.color("#aaaaaa")
        self.goto(0, 30)
        self.write("Use Arrow Keys to control the snake", align="center", font=("Arial", 14, "normal"))

        self.color("#555555")
        self.goto(0, -10)
        self.write("Eat food  •  Avoid walls  •  Don't bite yourself", align="center", font=("Arial", 12, "normal"))

    def show_game_over_screen(self, score, high_score):
        self.clear()

        self.color("#ff003c")
        self.goto(0, 130)
        self.write("GAME OVER", align="center", font=("Arial", 44, "bold"))

        self.color("#00fff7")
        self.goto(0, 60)
        self.write(f"Your Score:  {score}", align="center", font=("Arial", 26, "bold"))

        if score >= high_score and score > 0:
            self.color("#ffd700")
            self.goto(0, 15)
            self.write("🏆  New High Score!", align="center", font=("Arial", 16, "bold"))
        else:
            self.color("#888888")
            self.goto(0, 15)
            self.write(f"Best Score:  {high_score}", align="center", font=("Arial", 16, "normal"))

    def clear_overlay(self):
        self.clear()


# ==========================
# SCREEN SETUP
# ==========================
screen = Screen()
screen.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
screen.bgcolor(BG_COLOR)
screen.title("CYBER SNAKE 2077")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()
overlay = Overlay()

# Hide snake off screen initially
for seg in snake.segments:
    seg.goto(2000, 2000)

# ==========================
# GAME STATE
# ==========================
game_state = {"running": False, "over": False}


# ==========================
# BUTTON HELPERS (Tkinter embedded in Turtle canvas)
# ==========================
import tkinter as tk

canvas = screen.getcanvas()
root = canvas.winfo_toplevel()

btn_frame = tk.Frame(root, bg=BG_COLOR)

play_btn = tk.Button(
    btn_frame,
    text="▶  PLAY",
    font=("Arial", 18, "bold"),
    fg=BG_COLOR,
    bg=BUTTON_FG,
    activebackground="#00cccc",
    activeforeground=BG_COLOR,
    relief="flat",
    padx=36,
    pady=12,
    cursor="hand2",
    bd=0
)

restart_btn = tk.Button(
    btn_frame,
    text="↺  RESTART",
    font=("Arial", 18, "bold"),
    fg=BG_COLOR,
    bg="#ff00aa",
    activebackground="#cc0088",
    activeforeground=BG_COLOR,
    relief="flat",
    padx=36,
    pady=12,
    cursor="hand2",
    bd=0
)


def show_play_button():
    btn_frame.place(relx=0.5, rely=0.62, anchor="center")
    play_btn.grid(row=0, column=0)
    restart_btn.grid_forget()
    root.update()


def show_restart_button():
    btn_frame.place(relx=0.5, rely=0.64, anchor="center")
    restart_btn.grid(row=0, column=0)
    play_btn.grid_forget()
    root.update()


def hide_buttons():
    btn_frame.place_forget()
    root.update()


# ==========================
# GAME CONTROL FUNCTIONS
# ==========================
def start_game():
    game_state["running"] = True
    game_state["over"] = False

    overlay.clear_overlay()
    hide_buttons()

    snake.reset()
    for seg in snake.segments:
        seg.showturtle()

    food.show()
    scoreboard.show_hud()

    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    game_loop()


def restart_game():
    scoreboard.reset()
    start_game()


def end_game():
    game_state["running"] = False
    game_state["over"] = True

    food.hide_food()

    final_score = scoreboard.score
    if final_score > scoreboard.high_score:
        scoreboard.high_score = final_score

    scoreboard.clear_display()
    overlay.show_game_over_screen(final_score, scoreboard.high_score)
    screen.update()

    show_restart_button()


# ==========================
# MAIN GAME LOOP
# ==========================
def game_loop():
    if not game_state["running"]:
        return

    screen.update()
    snake.move()

    # Food collision
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Wall collision
    if (
        snake.head.xcor() > 340
        or snake.head.xcor() < -340
        or snake.head.ycor() > 340
        or snake.head.ycor() < -340
    ):
        end_game()
        return

    # Tail collision (skip the head)
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            end_game()
            return

    # Schedule next frame using Tkinter's after() — avoids blocking with time.sleep
    root.after(int(GAME_SPEED * 1000), game_loop)


# ==========================
# INITIAL START SCREEN
# ==========================
play_btn.config(command=start_game)
restart_btn.config(command=restart_game)

overlay.show_start_screen()
screen.update()
show_play_button()

root.mainloop()
