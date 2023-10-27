import pygame
import sys
import numpy as np
from random import randint


dis = [800,600]
cellDims = 10

lineW = 1

assert dis[0]%cellDims == 0
assert dis[1]%cellDims == 0

root = pygame.display.set_mode(dis)
clock = pygame.time.Clock()
FPS = 60

speed = 5

states = np.array([[randint(0,0) for i in range(dis[0]//cellDims)] for i in range(dis[1]//cellDims)])

def drawGrid(root):
    for x in range(0,dis[0],cellDims):
        pygame.draw.line(root,(255,255,255),(x,0),(x,dis[1]),lineW)

    for y in range(0,dis[1],cellDims):
        pygame.draw.line(root,(255,255,255),(0,y),(dis[0],y),lineW)


diffs = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]

def update():
    global states
    new = []

    for y,row in enumerate(states):
        new.append([])
        for x,val in enumerate(row):
            surrounding = 0

            for diff in diffs:
                if len(states[0]) > x+diff[0] > -1 and len(states) > y+diff[1] > -1:
                    if states[y+diff[1]][x+diff[0]] == 1:
                        surrounding += 1

            if states[y][x] == 1:
                if surrounding <= 1 or surrounding >= 4:
                    new[-1].append(0)
                else:
                    new[-1].append(1)

            else:
                if surrounding == 3:
                    new[-1].append(1)
                else:
                    new[-1].append(0)

    states = new.copy()

def main(args):
    global states

    pause = True

    frame = 0

    while True:
        frame += 1

        if frame == speed:
            frame= 0
        
        pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause = not pause
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pressed = True

        if not pause and frame == 0:
            update()

        if pause and pressed:
            mpos = pygame.mouse.get_pos()
            states[mpos[1]//cellDims][mpos[0]//cellDims] = int(not bool(states[mpos[1]//cellDims][mpos[0]//cellDims]))

        root.fill((0,0,0))

        for y,row in enumerate(states):
            for x,val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(root,(255,255,255),(x*cellDims,y*cellDims,cellDims,cellDims))

        if pause:
            drawGrid(root)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        pygame.quit()
        raise e

    pygame.quit()
