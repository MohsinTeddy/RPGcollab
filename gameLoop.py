import pygame
import math
from random import randint

def initLoop(screenSurf: pygame.Surface, filePathRoot: str):
    global loadedTiles
    global fileRoot
    global camPos
    global screen
    global tileGrid
    tileGrid = [[30,30],[],[],[]]
    for layer in range(len(tileGrid)-1):
        for i in range(tileGrid[0][0]):
            for i in range(tileGrid[0][1]):
                if layer != 0:
                    tileGrid[layer+1].append(0)
    for i in range(tileGrid[0][0]):
        tileGrid[1].append(2)
    for i in range(tileGrid[0][1]-2):
        tileGrid[1].append(2)
        for i in range(tileGrid[0][0]-2):
            tileGrid[1].append(1)
        tileGrid[1].append(2)
    for i in range(tileGrid[0][0]):
        tileGrid[1].append(2)
    screen = screenSurf
    camPos = [0,0]
    loadedTiles = []
    fileRoot = filePathRoot
    for i in range(3):
        loadedTiles.append(pygame.image.load(f'{fileRoot}Assets/Texture/Tile/t{i}.png'))

def renderTileType(Pos: tuple, Type: int):
    global loadedTiles
    tileSurf = loadedTiles[Type]
    screen.blit(tileSurf, Pos)

def renderTiles(layer: int):
    tileSize = 24
    gridData = tileGrid[layer+1]
    origTilePos = [-(camPos[0]%tileSize),-(camPos[1]%tileSize)]
    tilePos = [origTilePos[0],origTilePos[1]]
    renderWidth = math.floor(screen.get_width()/tileSize) + 1
    renderHeight = math.floor(screen.get_height()/tileSize) + 1
    gridWidth = tileGrid[0][0]
    gridHeight = tileGrid[0][1]
    tileOffX = math.floor(camPos[0]/tileSize)
    tileOffY = math.floor(camPos[1]/tileSize)
    tileID = tileOffX
    tileID += tileOffY*gridWidth
    for col in range(renderHeight):
        for row in range(renderWidth):
            tileType = 0
            if tileID >= 0:
                if tileID <= len(gridData)-1:
                    tileType = gridData[tileID]
            renderTileType(tilePos, tileType)
            tilePos[0] += tileSize
            tileID += 1
        tileID += gridWidth-renderWidth
        tilePos[0] = origTilePos[0]
        tilePos[1] += tileSize

def movePlayer():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camPos[1] -= 2 
    if keys[pygame.K_s]:
        camPos[1] += 2
    if keys[pygame.K_a]:
        camPos[0] -= 2
    if keys[pygame.K_d]:
        camPos[0] += 2

def tickLoop():
    renderTiles(0)
    movePlayer()