import pygame
import math
from random import randint

def initLoop(screenSurf: pygame.Surface, filePathRoot: str):
    global loadedTiles
    global invisTiles
    global fileRoot
    global camPos
    global screen
    global tileGrid
    global tileSize
    global tileBrush
    tileBrush = [3,0,'']
    tileSize = 24
    tileGrid = [[20,30],[],[],[]]
    for layer in range(len(tileGrid)-1):
        for i in range(tileGrid[0][0]):
            for i in range(tileGrid[0][1]):
                if layer != 0:
                    tileGrid[layer+1].append(0)
    for i in range(tileGrid[0][0]):
        tileGrid[1].append(3)
    for i in range(tileGrid[0][1]-2):
        tileGrid[1].append(3)
        for i in range(tileGrid[0][0]-2):
            tileGrid[1].append(randint(1,2))
        tileGrid[1].append(3)
    for i in range(tileGrid[0][0]):
        tileGrid[1].append(3)
    screen = screenSurf
    camPos = [0,0]
    loadedTiles = []
    fileRoot = filePathRoot
    for i in range(4):
        loadedTiles.append(pygame.image.load(f'{fileRoot}Assets/Texture/Tile/t{i}.png').convert_alpha())
    invisTiles = [0]

def renderTileType(Pos: tuple, Type: int):
    global loadedTiles
    global invisTiles
    if Type in invisTiles:
        return
    tileSurf = loadedTiles[Type]
    screen.blit(tileSurf, Pos)

def renderTiles(layer: int):
    global tileSize
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
    tileIdx = getTileIndex(pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camPos[1] -= 2 
    if keys[pygame.K_s]:
        camPos[1] += 2
    if keys[pygame.K_a]:
        camPos[0] -= 2
    if keys[pygame.K_d]:
        camPos[0] += 2
    if keys[pygame.K_e]:
        tileBrush[0] = tileGrid[tileBrush[1]+1][tileIdx]
    if keys[pygame.K_1]:
        tileBrush[1] = 0
    if keys[pygame.K_2]:
        tileBrush[1] = 1
    if keys[pygame.K_3]:
        tileBrush[1] = 2
    lockCamera()

def lockCamera():
    if camPos[0] < 0:
        camPos[0] = 0
    if camPos[1] < 0:
        camPos[1] = 0
    if camPos[0] > (tileGrid[0][0]*tileSize)-screen.get_width():
        camPos[0] = (tileGrid[0][0]*tileSize)-screen.get_width()
    if camPos[1] > (tileGrid[0][1]*tileSize)-screen.get_height():
        camPos[1] = (tileGrid[0][1]*tileSize)-screen.get_height()

def getTileIndex(Pos):
    global tileSize
    gridHeight = tileGrid[0][1]
    gridWidth = tileGrid[0][0]
    gridX = math.floor((Pos[0]+camPos[0])/tileSize)
    gridY = math.floor((Pos[1]+camPos[1])/tileSize)
    tileID = gridX+(gridY*gridWidth)
    return tileID

def tickLoop():
    global tileBrush
    renderTiles(0)
    renderTiles(1)
    renderTiles(2)
    tileIdx = getTileIndex(pygame.mouse.get_pos())
    if pygame.mouse.get_pressed()[0]:
        if tileIdx >= 0:
            if tileIdx <= len(tileGrid[tileBrush[1]+1])-1:
                print(tileGrid[1][tileIdx])
                tileGrid[tileBrush[1]+1][tileIdx] = tileBrush[0]
    movePlayer()