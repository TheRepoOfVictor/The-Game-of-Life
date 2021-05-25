import tkinter
import random
from tkinter.constants import TRUE
from typing import Text

# One day I came across Veritasium's "There's a Hole at the Bottom of Math" video on Youtube (https://www.youtube.com/watch?v=HeQX2HjkcNo).
# While it mosly talks about Mathematic's incompleteness and undecidability it also briefly mentioned Conway's Game of Life 
# (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) which inspired me to write this python scipt in one afternoon. 
# I found the pseudo-moving tiles in shown in the game facinating and the possible patterns incredibly beautiful and so I sought to create it myself

# After searching around Google for a good simple GUI library for Python I came across tkinter which is what I ended up using. 
# The "World" or canvas of the game is 100 tall by 200 wide with each cell being 5 by 5 pixels. I added the option to randomize the world since I didn't
# want to click every cell I want alive though it might be good to add that functionality later to create my own set patterns.
# There is a problem with the tkinter's "canvas.create_rectangle" method which is used to draw all the cells that is really apparent when it needs to draw
# a lot of cells at once, which happens very commonly at the beginning of the game. My assumption is that every call to the method will only draw one cell
# requiring hundreds if not thousands of calls which definitely slows things down. Perhaps another GUI library that allows adding the to-be-drawn shapes
# to a queue and the call to draw them happens only once will speed things up. 

height = 100
width = 200

class cell:
    count = 0
    def __init__(self, x, y, live = False):
        self.x = x
        self.y = y
        self.alive = live

class world:
    cells = []
    def __init__(self, wid, len):
        self.len = len
        self.wid = wid
        for x in range(0, self.wid):
            cellRow = []
            for y in range(0, self.len):
                c = cell(x, y)
                cellRow.append(c)
                    
            self.cells.append(cellRow)

    def clearWorld(self):
        for cr in self.cells:
            for c in cr:
                c.alive = False

    def clearCount(self):
        for cr in self.cells:
            for c in cr:
                c.count = 0

    def populateCells(self, cx, cy):
        for x in range(cx-1, cx+2):
            for y in range(cy-1, cy+2):
                if not (x == cx and y == cy):
                    self.cells[x % self.wid][y % self.len].count += 1

theWorld = world(width, height)

def drawWorld():
    for cr in theWorld.cells:
        for c in cr:
            if c.alive:
                canvas.create_rectangle(c.x*5, c.y*5, c.x*5+5, c.y*5+5, outline="black", fill="black")

def RandomizeWorld():
    canvas.delete("all")
    theWorld.clearWorld()

    max = width * height
    num_cells = random.randint(max/2,max)
    for x in range(num_cells):
        randx = random.randint(0, width - 1)
        randy = random.randint(0, height - 1)
        theWorld.cells[randx][randy].alive = True
    drawWorld()

stop = False
def BeginLife():
    global stop 
    stop = False
    while(not stop):
        top.update()
        canvas.delete("all")
        theWorld.clearCount()

        for cr in theWorld.cells:
            for c in cr:
                if c.alive:
                    theWorld.populateCells(c.x, c.y)

        for cr in theWorld.cells:
            for c in cr:
                if c.alive:
                    if c.count < 2 or c.count > 3:
                        c.alive = False
                else:
                    if c.count == 3:
                        c.alive = True

        drawWorld()

def PauseLife():
    global stop
    stop = True

top = tkinter.Tk()
top.title("Life")

canvas = tkinter.Canvas(top, bg="white", height=height*5, width=width*5)
canvas.pack()

button2 = tkinter.Button(top, text="Randomize", command = RandomizeWorld)
button2.pack()
button1 = tkinter.Button(top, text="Begin", command = BeginLife)
button1.pack()
button3 = tkinter.Button(top, text="Pause", command = PauseLife)
button3.pack()

drawWorld()
top.mainloop()
