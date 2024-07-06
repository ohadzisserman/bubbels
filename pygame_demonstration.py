import pygame as pg
from pygame.draw import circle, line, polygon, rect
from math import sin, pi
from time import sleep
pg.font.init()
pg.init()


###  dispaly parameters ###
#dimentions of the display
W,H = 2000,1000
screen = pg.display.set_mode((W,H))
#center: usefull for shifting
cx = 1000
cy = 500

### simulation parameters setup ###
N = 200 #Number of points in the rope
rope = [7*sin(pi*i/70) for i in range(N)] #y axis position of each dot
#rope = [7*(i>N//2-20)*(i<N//2+20)*(sin(2*pi*(i-N//2)/40)) for i in range(N)]
rope_speed = [0 for i in range(N)]
def draw():
    m = max([abs(i) for i in rope_speed])
    # for i in range(N):
    #      B = int(250*abs(rope_speed[i]/m))
    #      circle(screen, [255,B,B],(i*W/N,cy+10*rope[i]),5)
    for i in range(N-1):
        line(screen, [255,0,int(250*abs(rope_speed[i]/m))],(i*W/N,cy+10*rope[i]),((i+1)*W/N,cy+10*rope[i+1]),2)
    for i in range(1,N-1):
        #speed
        line(screen, [255, 255, 0], (i * W / N, cy + 10 * rope[i]),
             ((i) * W / N, cy + 10 * (rope[i] + rope_speed[i]*15)), 2)
        circle(screen, [255, 0, 0],
             (1+(i) * W / N,  cy + 10 * (rope[i] + rope_speed[i] * 15)), 3)
    #     #acceloration
    #     line(screen, [0,0, 255], (i * W / N,-50*((rope[i]-rope[i-1]) + (rope[i]-rope[i+1]))+ cy + 10 * rope[i]),
    #          ((i) * W / N, cy + 10 * (rope[i] + rope_speed[i] * 15)), 1)


def next():
    for i in range(1,N-1):#update speed according to the shape of the string
        rope_speed[i] -= (rope[i]-rope[i-1]) + (rope[i]-rope[i+1])
    for i in range(1,N-1):
        rope[i] += rope_speed[i]

### main loop ###
while True:
    screen.fill(0) #paints the display black
    next() #preforme the phisical iteration
    draw() #paint the display with the simulated data
    sleep(0.001) #create a delay
    pg.display.flip() #update the display