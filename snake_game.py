import pygame as pg
import sys,random
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *

pg.init()

#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

class snake(object):
    global rows, width , c, flag
    body = []
    turns = {}
    def __init__(self,color,pos):
        self.color = color
        self.head = Cube(pos, color)
        self.body.append(self.head)

    def move (self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
        keys = pg.key.get_pressed()
        prev_position_list = self.prev_pos_list()
        if keys[pg.K_LEFT]:
            dirx = -1
            diry = 0
            self.turns[self.head.pos[:]]=[dirx,diry]
            for i,b in enumerate(self.body):
                p = b.pos
                if i==0:
                    if p in self.turns:
                        b.move(dirx,diry)
                        self.crash_head_to_tail()
                        self.addCube()
                        self.border_check(i)
                elif i!=0:
                    self.tail_logic(i, prev_position_list)

        elif keys[pg.K_RIGHT]:
            dirx = 1
            diry = 0
            self.turns[self.head.pos[:]] = [dirx,diry]
            for i, b in enumerate(self.body):
                p = b.pos
                if i==0:
                    if p in self.turns:
                        b.move(dirx,diry)
                        self.crash_head_to_tail()
                        self.addCube()
                        self.border_check(i)

                elif i!=0:
                    self.tail_logic(i, prev_position_list)

        elif keys[pg.K_UP]:
            dirx = 0
            diry = -1
            self.turns[self.head.pos[:]] = [dirx,diry]
            for i, b in enumerate(self.body):
                p = b.pos
                if i==0:
                    if p in self.turns:
                        b.move(dirx,diry)
                        self.crash_head_to_tail()
                        self.addCube()
                        self.border_check(i)
                elif i!=0:
                    self.tail_logic(i, prev_position_list)

        elif keys[pg.K_DOWN]:
            dirx = 0
            diry = 1
            self.turns[self.head.pos[:]] = [dirx,diry]
            for i, b in enumerate(self.body):
                p = b.pos
                if i==0:
                    if p in self.turns:
                        b.move(dirx,diry)
                        self.crash_head_to_tail()
                        self.addCube()
                        self.border_check(i)
                elif i!=0:
                    self.tail_logic(i, prev_position_list)

    def crash_head_to_tail(self):
        headOfSnake = self.body[0]
        for i,n in enumerate(self.body):
            if i > 0:
                if headOfSnake.pos[:] == n.pos[:]:
                    messageBox("You lost!","Your score is "+str(len(self.body))+"\n  Play again!")
                    self.reset(self.body)

    def tail_logic (self, i, previos_positions):
        tailCube = self.body[i]
        dirxDelta = previos_positions[i-1][0] - tailCube.pos[0]
        diryDelta = previos_positions[i-1][1] - tailCube.pos[1]
        tailCube.move(dirxDelta,diryDelta)

    def prev_pos_list (self):
        pos_list = []
        for i,n in enumerate(self.body):
            pos_list.append(n.pos[:])
        return pos_list

    def reset (self, body):
        body.clear()
        self.head = Cube((10,10), color=RED)
        body.append(self.head)

    def addCube(self):
        global c,tickValue
        headOfSnake = self.body[0] #head of snake
        if headOfSnake.pos[:] == c.pos[:]:
            self.body.append(Cube(headOfSnake.pos[:],color=RED))
            if len(self.body) % 10 == 0 :
                tickValue+=5
            c.randomDraw()

    def draw(self, surf):
        if len(self.body) > 0 :
            for i,n in enumerate(self.body):
                eyes =False   # eyes for snake
                if i==0:
                    eyes =True
                    n.draw(surf,eyes)
                n.draw(surf,eyes)

    def border_check (self,i):
        bottom_border = right_border = (width//(width//rows))
        upper_border = left_border = 0
        headOfSnake = self.body[i]
        if headOfSnake.pos[i] > right_border-1 :
            headOfSnake.move(-right_border,0)

        if headOfSnake.pos[i+1] > bottom_border-1 :
            headOfSnake.move(0,-bottom_border)

        if headOfSnake.pos[i+1] < upper_border:
            headOfSnake.move(0,bottom_border)

        if headOfSnake.pos[i] < left_border:
            headOfSnake.move(right_border,0)

class Cube(object):
    global rows,width,s
    def __init__(self, start,color, dirnx=1, dirny=0):
        self.pos = start
        self.color = color

    def draw(self,surface, eyes):
        distance = width // rows
        i = self.pos[0]
        j = self.pos[1]
        if eyes:
            pg.draw.rect(surface,self.color,(i*distance+1,j*distance+1,distance-1,distance-1))
            pg.draw.circle(surface,BLACK,(i*distance+8,j*distance+10),2,2)
            pg.draw.circle(surface,BLACK,(i*distance+17,j*distance+10),2,2)
        else:
             pg.draw.rect(surface,self.color,(i*distance+1,j*distance+1,distance-1,distance-1))

    def randomDraw (self):
        distance = width // (width // rows)
        snak_pos = (random.randrange(distance),random.randrange(distance))
        snake_body_pos = []
        for i,n in enumerate(s.body):
            snake_body_pos.append(n.pos)
        while snak_pos in snake_body_pos:
            snak_pos = (random.randrange(distance),random.randrange(distance))
        self.pos = snak_pos

    def move(self,dirx,diry):
        newPos = (self.pos[0]+dirx,self.pos[1]+diry)
        self.pos=newPos

def messageBox(subject, content):
        root = tk.Tk()
        root.attributes("-topmost",True)
        root.withdraw()
        messagebox.showinfo(subject,content)
        try:
            root.destroy()
        except :
            pass


def drawtheGrid(width,rows,surface):
    w = width // rows
    pos_x = 0
    pos_y = 0
    lineX =0
    lineY = 0
    for i in range(rows):
        lineX+=pos_x + w
        lineY+=pos_y + w
        pg.draw.line(surface,WHITE,(lineX,0),(lineX,width))
        pg.draw.line(surface,WHITE,(0,lineY),(width,lineY))

def redrawWindow(surface):
    global rows, width, s, c
    surface.fill(BLACK)
    drawtheGrid(width,rows,surface)
    c.draw(surface,False)
    s.draw(surface)
    pg.display.update()

def main():
    global rows, width, s, c, flag,tickValue
    width = 500
    rows = 20
    pg.display.set_caption('Snake')
    DISPLAYSURF = pg.display.set_mode((width,width))
    s = snake(RED,(10,10))
    c = Cube((10,13),color=WHITE)
    fpsClock = pg.time.Clock()
    FPS = 30
    flag =True
    delay = 10
    tickValue = 10
    while flag:
        pg.time.delay(10)
        fpsClock.tick(tickValue)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        s.move()
        redrawWindow(DISPLAYSURF)
main()
