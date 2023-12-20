"""
########################################################################
#
#  2048 Python implementation
#
#  Copyright 2023 - NGUYEN Aymeric, LOUFOUA Samuel, THIBAULT Paul
#
#  This program is free software; you can redistribute it  and/or
#  modify it under the terms of the Send  Me  a  Postcard  Public
#  License for Open Source.
#
#  You can send your postcard to this address :
#    M. NGUYEN Aymeric
#    24 RUE FRANCOIS VAUDIN
#    95450 ABLEIGES
#
########################################################################
"""
#!/usr/bin/env python
import random
import tkinter
import math

WIDTH = 600
HEIGHT = WIDTH
SPACING = WIDTH/60
TILE_WIDTH = (WIDTH - 2*SPACING)/4

def main():
    global mainWindow
    global uiTiles
    global labels
    global tileColors
    global textColors
    global grid
    global message
    global movesLabel
    global scoreLabel
    global isGameOver
    global moveCounter
    global tiles
    global score

    isGameOver  = False
    moveCounter = 0
    tiles       = [0] * 16
    score       = 0
    moves       = 0
    uiTiles     = [None] * 16 # background color of our tiles
    labels      = [None] * 16 # labels of our tiles
    tileColors  = ['antique white', 'bisque', 'dark salmon', 'salmon', 'tomato', 'orange red', 'red', 'light goldenrod', 'dark goldenrod', 'yellow', 'blue']
    textColors  = ['NavajoWhite4','NavajoWhite4','white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']

    mainWindow = tkinter.Tk()
    mainWindow.title("2048")
    grid = tkinter.Canvas(mainWindow, width=WIDTH, height=HEIGHT, background='floral white')
    grid.pack()
    message = tkinter.Label(mainWindow, text='Press Left | Right | Up | Down')
    message.pack()
    scoreLabel = tkinter.Label(mainWindow, text=f'Score : {score}')
    scoreLabel.pack(side='left')
    movesLabel = tkinter.Label(mainWindow, text=f'Moves : {moves}')
    movesLabel.pack(side='right')
    initGrid()
    resetGame()
    mainWindow.bind('<Key>', onKeyPressed)
    mainWindow.mainloop()

def addRandomTile():
    '''TODO : Find an empty spot in `tiles` and fill it with 2 or 4.
    return True if success or False if no empty spot available'''
    return True

def noValidMove():
    '''TODO : return False if two adjacent cells have the same value, True otherwise.'''
    return False

def moveUpOnColumn(j):
    '''TODO : Pack `tiles` to the top, merge adjacent tiles to the top.
    If any new tile is created, increment `score` by the value of the new tile.'''

def moveRightOnLine(i):
    '''TODO : Pack `tiles` to the right, merge adjacent tiles to the right.
    If any new tile is created, increment `score` by the value of the new tile.'''
    
def moveDownOnColumn(j):
    '''TODO : Pack `tiles` to the bottom, merge adjacent tiles to the bottom.
    If any new tile is created, increment `score` by the value of the new tile.'''

def moveLeftOnLine(i):
    '''TODO : Pack `tiles` to the left, merge adjacent tiles to the left.
    If any new tile is created, increment `score` by the value of the new tile.'''

def createTile(i, j):
    dx = (j * TILE_WIDTH + SPACING) + SPACING
    dy = (i * TILE_WIDTH + SPACING) + SPACING
    uiTiles[4*i+j] = grid.create_rectangle(dx, dy, dx + TILE_WIDTH-SPACING, dy + TILE_WIDTH-SPACING, width=0)
    labels[4*i+j] = grid.create_text(dx + TILE_WIDTH/2, dy + TILE_WIDTH/2, text='')
    return uiTiles[4*i+j]

def resetGame():
    global moveCounter
    global isGameOver
    moveCounter = 0
    isGameOver = False
    for i in range (0,16):
        tiles[i] = 0
    addRandomTile()
    addRandomTile()
    updateGrid()
    
def initGrid():
    for i in range (0,4):
        for j in range (0,4):
            createTile(i, j)

def gameOver():
    global isGameOver
    isGameOver = True

def apply(applyDirectionalOp):
    global moveCounter
    global isGameOver
    before = str(tiles)
    for i in range (0,4):
        applyDirectionalOp(i)
    after = str(tiles)
    hasChanged = before != after
    if hasChanged:
        moveCounter += 1
        addRandomTile()
        if noValidMove():
            gameOver()
        updateGrid()

def playLeft():
    apply(moveLeftOnLine)

def playRight():
    apply(moveRightOnLine)

def playDown():
    apply(moveDownOnColumn)

def playUp():
    apply(moveUpOnColumn)

def updateGrid():
    updateTiles()
    updateScore()
    updateMoves()
    if isGameOver:
        updateMessage("GAME OVER ! Press Enter to start a new game.")
    else:
        updateMessage('')
        
def updateTiles():
    for i in range(0, 4):
        for j in range (0, 4):
            updateTile(i, j, tiles[4*i+j])

def updateTile(i, j, value):
    display = '' if value == 0 else str(value)
    level = int(math.log2(value+1))
    grid.itemconfigure(labels[4*i+j], text=display, font=("Arial", 20 + level), fill=textColors[level])
    grid.itemconfigure(uiTiles[4*i+j], fill=tileColors[level])

def updateMessage(msg):
  message['text'] = msg

def updateScore():
    scoreLabel['text'] = f'Score : {score}'

def updateMoves():
    movesLabel['text'] = f'{str(moveCounter)} Moves'

def onKeyPressed(event):
  if isGameOver and event.keysym != "Return":
    return
  match event.keysym:
    case "Left":
      playLeft()
    case "Right":
      playRight()
    case "Up":
      playUp()
    case "Down":
      playDown()
    case "Return":
      resetGame()
    case _:
      updateMessage("Invalid key pressed: %s" % event.keysym)

if __name__ == '__main__':
    main()