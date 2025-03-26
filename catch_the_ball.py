import tkinter as tk
import random

class CatchTheBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Ball Game")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="black")
        self.canvas.pack()

        # Paddle
        self.paddle_width = 100
        self.paddle_height = 10  # Reduced height
        self.paddle = self.canvas.create_rectangle(200, 350, 200 + self.paddle_width, 350 + self.paddle_height, fill="cyan", outline="white")

        # Ball
        self.ball = self.canvas.create_oval(245, 50, 255, 60, fill="yellow")

        # Variables
        self.ball_speed = 5
        self.paddle_speed = 15
        self.ball_direction = [random.choice([-3, 3]), self.ball_speed]
        self.score = 0
        self.lives = 3
        self.moving_left = False
        self.moving_right = False

        # Score and lives display
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 12), fg="white", bg="black")
        self.score_label.pack(side="left", padx=10)
        self.lives_label = tk.Label(root, text=f"Lives: {self.lives}", font=("Arial", 12), fg="white", bg="black")
        self.lives_label.pack(side="right", padx=10)

        # Bind keys
        self.root.bind("<Left>", self.start_moving_left)
        self.root.bind("<Right>", self.start_moving_right)
        self.root.bind("<KeyRelease-Left>", self.stop_moving)
        self.root.bind("<KeyRelease-Right>", self.stop_moving)

        self.restart_button = None

        # Start game loop
        self.update_game()
        self.move_paddle()

    def start_moving_left(self, event):
        self.moving_left = True

    def start_moving_right(self, event):
        self.moving_right = True

    def stop_moving(self, event):
        self.moving_left = False
        self.moving_right = False

    def move_paddle(self):
        x1, _, x2, _ = self.canvas.coords(self.paddle)
        if self.moving_left and x1 > 0:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)
        if self.moving_right and x2 < 500:
            self.canvas.move(self.paddle, self.paddle_speed, 0)
        self.root.after(20, self.move_paddle)

    def update_game(self):
        self.canvas.move(self.ball, self.ball_direction[0], self.ball_direction[1])
        ball_coords = self.canvas.coords(self.ball)

        # Ball collision with walls
        if ball_coords[0] <= 0 or ball_coords[2] >= 500:
            self.ball_direction[0] = -self.ball_direction[0]
        if ball_coords[1] <= 0:
            self.ball_direction[1] = self.ball_speed

        paddle_coords = self.canvas.coords(self.paddle)
        if (
            ball_coords[2] >= paddle_coords[0]
            and ball_coords[0] <= paddle_coords[2]
            and ball_coords[3] >= paddle_coords[1]
        ):
            self.ball_direction[1] = -self.ball_speed
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.move(self.ball, 0, -10)  # Bounce effect

            if self.score % 5 == 0:
                self.ball_speed += 1
                self.paddle_speed += 1
                self.paddle_width = max(50, self.paddle_width - 10)  # Reduce paddle size
                self.canvas.coords(self.paddle, paddle_coords[0], paddle_coords[1], paddle_coords[0] + self.paddle_width, paddle_coords[1] + self.paddle_height)

        if ball_coords[3] >= 400:
            self.lives -= 1
            self.lives_label.config(text=f"Lives: {self.lives}")
            self.reset_ball()

        if self.lives > 0:
            self.root.after(30, self.update_game)
        else:
            self.end_game()

    def reset_ball(self):
        self.canvas.coords(self.ball, 245, 50, 255, 60)
        self.ball_direction = [random.choice([-3, 3]), self.ball_speed]

    def end_game(self):
        self.canvas.create_rectangle(0, 0, 500, 400, fill="red", stipple="gray50")  # Flash effect
        self.canvas.create_text(250, 200, text="Game Over", font=("Arial", 24), fill="white")
        self.canvas.create_text(250, 240, text=f"Your Score: {self.score}", font=("Arial", 18), fill="white")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")

        if self.restart_button is None:
            self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.restart_game, bg="gray", fg="white")
            self.restart_button.pack(pady=20)

    def restart_game(self):
        self.score = 0
        self.lives = 3
        self.ball_speed = 5
        self.paddle_speed = 15
        self.paddle_width = 100
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.canvas.delete("all")

        self.paddle = self.canvas.create_rectangle(200, 350, 200 + self.paddle_width, 350 + self.paddle_height, fill="cyan", outline="white")
        self.ball = self.canvas.create_oval(245, 50, 255, 60, fill="yellow")
        self.ball_direction = [random.choice([-3, 3]), self.ball_speed]

        self.root.bind("<Left>", self.start_moving_left)
        self.root.bind("<Right>", self.start_moving_right)
        self.root.bind("<KeyRelease-Left>", self.stop_moving)
        self.root.bind("<KeyRelease-Right>", self.stop_moving)

        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None

        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = CatchTheBallGame(root)
    root.mainloop()
