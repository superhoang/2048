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
    tileColors  = ['#eee4da', '#eee4da', '#ede0c8', '#f2b179', '#f59563', '#f67c5f', '#f65e3b', '#edcf72', '#edcc61', '#edc850', '#edc53f', '#edc22e']
    textColors  = ['NavajoWhite4','NavajoWhite4','white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']

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
    if not 0 in tiles:
        return False
    r = random.randint(0,15)
    while tiles[r]!= 0:
        r = random.randint(0,15)
    tiles[r] = random.randint(1,2)*2
    return True

def noValidMove():
    if 0 in tiles:
        return False
    for i in range(0,4):
        if hasValidMoveLine(i):
            return False
    for j in range(0,4):
        if hasValidMoveColumn(j):
            return False
    return True

def hasValidMoveColumn(j):
    for i in range(0,3):
        if tiles[4*i+j] == tiles[4*i+j+4]:
            return True
    return False

def hasValidMoveLine(i):
    for j in range(0,3):
        if tiles[4*i+j] == tiles[4*i+j+1]:
            return True
    return False

def packColumnUp(j):
    for i in range(3):
        if sum(tiles[j+i*4:16:4]) == 0:
            return
        else:
            while tiles[j+4*i] == 0:
                tiles[j+i*4:16:4] = tiles[j+i*4+4:16:4] + [0]

def moveUpOnColumn(j):
    '''Pack `tiles` to the top, merge adjacent tiles to the top.
    If any new tile is created, increment `score` by the value of the new tile.'''
    packColumnUp(j)
    mergeColumnUp(j)
    packColumnUp(j)

def mergeColumnUp(j):
    global score
    for i in range(0,3):
        if tiles[0+j+4*i] == tiles[4+j+4*i] and tiles[4+j+4*i] != 0:
            tiles[0+j+4*i] *= 2
            tiles[4+j+4*i] = 0
            score += tiles[0+j+4*i]
    
def packLineRight(i):
    for j in range(3):
        if sum(tiles[i*4:i*4+4-j]) == 0:
            return
        else:
            while tiles[i * 4 - j + 3] == 0:
                tiles[i*4:i*4+4-j] = [0] + tiles[i*4:i*4+3-j]

def mergeLineRight(i):
    global score
    for j in range(3):
        if tiles[i*4+3-j] == tiles[i*4+2-j]:
            tiles[i*4+2-j] = 0
            tiles[i*4+3-j] *= 2
            score += tiles[i*4+3-j]

def moveRightOnLine(i):
    '''Pack `tiles` to the right, merge adjacent tiles to the right.
    If any new tile is created, increment `score` by the value of the new tile.'''
    packLineRight(i)
    mergeLineRight(i)
    packLineRight(i)
    
def packColumnDown(j):
    for i in range(3):
        if sum(tiles[j:16-4*i:4]) == 0:
            return
        else:
            while tiles[12+j-4*i] == 0:
                tiles[j:16-4*i:4] = [0] + tiles[j:12-4*i:4]

def moveDownOnColumn(j):
    '''Pack `tiles` to the bottom, merge adjacent tiles to the bottom.
    If any new tile is created, increment `score` by the value of the new tile.'''
    packColumnDown(j)
    mergeColumnDown(j)
    packColumnDown(j)

def mergeColumnDown(j):
    global score
    for i in range(0,3):
        if tiles[12+j-4*i] == tiles[8+j-4*i] and tiles[8+j-4*i] != 0:
            tiles[12+j-4*i] *= 2
            tiles[8+j-4*i] = 0
            score += tiles[12+j-4*i]

def packLineLeft(i):
    for j in range(3):
        if sum(tiles[i * 4 + j : i * 4 + 4]) == 0:
            return
        else:
            while tiles[i * 4 + j] == 0:
                tiles[i * 4 + j : i * 4 + 4] = tiles[i * 4 + j + 1 : i * 4 + 4] + [0]

def mergeLineLeft(i):
    global score
    for j in range(3):
        if tiles[i*4+j] == tiles[i*4+j+1] and tiles[i*4+j] != 0:
            tiles[i*4+j+1] = 0
            tiles[i*4+j] *= 2
            score +=  tiles[i*4+j]

def moveLeftOnLine(i):
    '''Pack `tiles` to the left, merge adjacent tiles to the left.
    If any new tile is created, increment `score` by the value of the new tile.'''
    packLineLeft(i)
    mergeLineLeft(i)
    packLineLeft(i)

def createTile(i, j):
    dx = (j * TILE_WIDTH + SPACING) + SPACING
    dy = (i * TILE_WIDTH + SPACING) + SPACING
    uiTiles[4*i+j] = grid.create_rectangle(dx, dy, dx + TILE_WIDTH-SPACING, dy + TILE_WIDTH-SPACING, width=0)
    labels[4*i+j] = grid.create_text(dx + TILE_WIDTH/2, dy + TILE_WIDTH/2, text='')
    return uiTiles[4*i+j]

def resetGame():
    global score
    global moveCounter
    global isGameOver
    global score
    moveCounter = 0
    isGameOver = False
    score = 0
    for i in range (0,16):
        tiles[i] = 0
    addRandomTile()
    addRandomTile()
    score = 0
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
    grid.itemconfigure(labels[4*i+j], text=display, font=("Arial", 20 + level), fill=textColors[level % len(textColors)])
    grid.itemconfigure(uiTiles[4*i+j], fill=tileColors[level % len(tileColors)])

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
