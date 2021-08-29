from tkinter import *
import random

WIDTH = 900
HEIGHT = 300
# score for players
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
# speed limit
INITIAL_SPEED = 20
# pad stats
# Pad width
PAD_W = 10
# pad height
PAD_H = 100
# ball stats
# ball radius
BALL_RADIUS = 30
# ball speed
# horiz speed
BALL_X_CHANGE = 20
# vertical speed
BALL_Y_CHANGE = 0
# window
root = Tk()
root.title("PingPong Game")
# canvas
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#008b8b")
c.pack()
# left line
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# right line
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
# center line
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")
# create ball
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2, fill="#FF4500")
# PADS
# left pad
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="white")
# right pad
RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, width=PAD_W, fill="white")
#SCORES
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font='Arial 20',
                         fill='yellow')
p_2_text = c.create_text(WIDTH / 6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font='Arial 20',
                         fill='yellow')
# pad speed
PAD_SPEED = 20
# right pad speed
RIGHT_PAD_SPEED = 0
# left pad speed
LEFT_PAD_SPEED = 0
# ball speed after recoshet
BALL_SPEED_UP = 1.00
# max  ball speed
BALL_MAX_SPEED = 30
# start ball speed horyz
BALL_X_SPEED = 20
# start ball speed verty
BALL_Y_SPEED = 20
# distance from right side
right_line_distance = WIDTH - PAD_W
# score list
def update_score(player):
    global  PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
# respawn
def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)
# Rycosheet from pads
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED
# func ball move
def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot)/2
    # vertycal rec
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH /2:
            if c.coords(RIGHT_PAD) [1] < ball_center < c.coords(RIGHT_PAD) [3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > WIDTH/2:
            c.move(BALL, right_line_distance - ball_right,BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')
# func pad move
def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])
def main():
    move_ball()
    move_pads()
    # self call
    root.after(30, main)
c.focus_set()
# key click
def moveent_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
# canvans releat key
c.bind("<KeyPress>", moveent_handler)
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0
c.bind("<KeyRelease>", stop_pad)
# start
main()
# start window
root.mainloop()
