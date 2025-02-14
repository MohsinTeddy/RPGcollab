import pygame
import math
import gui
import tileProperties
from random import randint

def regenViewPort():
    global viewportSurfs 
    global viewportRects
    global gridPos
    viewportRects = []
    viewportRects.append(pygame.Rect((0,gridPos[1]),(gridPos[0], screen.get_height()-gridPos[1]-gridPos[3])))
    viewportRects.append(pygame.Rect((screen.get_width()-gridPos[2],gridPos[1]),(gridPos[2], screen.get_height()-gridPos[1]-gridPos[3])))
    viewportRects.append(pygame.Rect((0,0),(screen.get_width(), gridPos[1])))
    viewportRects.append(pygame.Rect((0,screen.get_height()-gridPos[3]),(screen.get_width(), gridPos[3])))
    viewportSurfs = []
    for i in range(len(viewportRects)):
        viewportSurfs.append(pygame.Surface((viewportRects[i].width, viewportRects[i].height)))
        viewportSurfs[i].fill((255, 0, 0))

def initLoop(screenSurf: pygame.Surface, filePathRoot: str):
    global loadedTiles
    global fileRoot
    global camPos
    global screen
    global tileGrid
    global tileSize
    global tileBrush
    global playerSurfs
    global playerRect
    global playerPos
    global gridZoom
    global renderedObjects
    global gridPos
    global globalFrame
    #Initilizes important Variables
    globalFrame = 0
    screen = screenSurf
    fileRoot = filePathRoot # File Root explained in main.py
    gridZoom = 1
    gridPos = [24,24,24*4,0]
    gridPos = [0,32,0,0]
    regenViewPort()
    loadSprites()
    renderedObjects = []

    tileBrush = [6,0,'',0]  #[0] Tile ID [1] Grid Layer [2] Tile Data (This does nothing right now but keep it as '') [3] Grid Depth
    tileGrid = [[24,16]]

    # [0] Grid Properties
        # [0] Grid Size
            # [0] Grid Width
            # [1] Grid Height
    # [1...] Depth Data
        # [0] DepthNum
        # [1...] Layer
            # [1...] Tile
                # [0]: Tile ID
                # [1]: Tile Data

    for depth in range(2):
        tileGrid.append([depth]) # Creates a New Depth
        for layer in range(3):
            tileGrid[depth+1].append([]) # Creates a New Layer for each Depth
            for i in range(tileGrid[0][0]):
                for i in range(tileGrid[0][1]):
                    if layer == 0:
                        tileGrid[depth+1][layer+1].append([6,'']) # Fills each Layer of each Depth with Tile 6 (Table)
                    else:
                        tileGrid[depth+1][layer+1].append([0,'']) # Fills each Layer of each Depth with Tile 0 (Air)

    # Makes Depth 0, Layer 0 into a box like shape
    tileGrid[1][1] = []
    for i in range(tileGrid[0][0]):
        tileGrid[1][1].append([3,''])
    for i in range(tileGrid[0][1]-2):
        tileGrid[1][1].append([3,''])
        for i in range(tileGrid[0][0]-2):
            tileGrid[1][1].append([randint(1,2),''])
        tileGrid[1][1].append([3,''])
    for i in range(tileGrid[0][0]):
        tileGrid[1][1].append([3,''])

    camPos = [0,0]
    playerPos = [48,48]

class OptionSurfs():
    def __init__(self, origSurf: pygame.Surface):
        self.main = origSurf
        self.shadow = pygame.Surface.copy(self.main)
        self.shadow = self.main.convert_alpha()
        self.shadow = pygame.transform.flip(self.shadow, False, True)
        self.shadow.fill((0, 0, 0, 0), special_flags=pygame.BLEND_MULT)
        self.shadow.set_alpha(round(255/5))

def loadSprites():
    global playerSurfs
    global tileSize
    global scaleTileSize
    global playerRect
    global loadedTiles
    global gridZoom
    global selectorTiles

    #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    tileSize = 24
    scaleTileSize = math.ceil(tileSize* gridZoom)

    playerSurfs = pygame.image.load(f'{fileRoot}Assets/Texture/Player/test2.png').convert_alpha()
    playerSurfs = pygame.transform.scale(playerSurfs, (playerSurfs.get_width()*gridZoom, playerSurfs.get_height()*gridZoom))
    playerRect = playerSurfs.get_rect()
    
    selectorTiles = []
    for i in range(2):
        selectorTiles.append(pygame.image.load(f'{fileRoot}Assets/Texture/Tile/tSelector{i}.png'))
        selectorTiles[i] = selectorTiles[i].convert_alpha()
        selectorTiles[i] = pygame.transform.scale(selectorTiles[i], (math.ceil((tileSize+2)* gridZoom), math.ceil((tileSize+2)* gridZoom)))
        selectorTiles[i] = OptionSurfs(selectorTiles[i])
    loadedTiles = [] # Loads Tile Surfaces
    for i in range(8):
        hasAlpha = tileProperties.get(i,'alpha')
        loadedTiles.append(pygame.image.load(f'{fileRoot}Assets/Texture/Tile/t{i}.png'))
        if hasAlpha:
            loadedTiles[i] = loadedTiles[i].convert_alpha()
        else:
            loadedTiles[i] = loadedTiles[i].convert()
        if scaleTileSize != 24:
            loadedTiles[i] = pygame.transform.scale(loadedTiles[i], (scaleTileSize, scaleTileSize))
        loadedTiles[i] = OptionSurfs(loadedTiles[i])

def renderTileType(Pos: tuple, Type: int, Depth: int, Layer: int):
    global loadedTiles
    #Just Renders a tile at a position unless it is invisible (Like Tile 0)
    if not tileProperties.get(Type,'render'):
        return
    tileSurf = loadedTiles[Type]
    screen.blit(tileSurf.main, (Pos[0], Pos[1]))# - (Depth*scaleTileSize)))
    #if Depth > 0:
    #    screen.blit(tileSurf.shadow, (Pos[0], Pos[1] + scaleTileSize))

def renderAllObjectatRow(row, depth):
    for i in range(len(renderedObjects)):
        objData = renderedObjects[i]
        if depth == renderedObjects[i][3]:
            
            if row == math.floor((objData[2][1])/tileSize):
                print(f'{row}, {math.floor((objData[2][1])/tileSize)}')
                screen.blit(objData[0], objData[1])
                #pygame.display.update()
                #breakpoint()
                

def renderTiles(depth: int):
    global tileSize
    global gridPos
    # You don't really need to understand how it works in depth
    # It renders left to right, then goes down and repeats
    # Is also optimised to not include tiles that do not fit in the viewport
    origTilePos = [-(camPos[0]%scaleTileSize)+gridPos[0],-(camPos[1]%scaleTileSize)+gridPos[1]]
    #origTilePos[1] += depth * scaleTileSize
    safteyMargin = 2 # An extra row and column of tiles to be generated
    renderWidth = math.floor((screen.get_width()-gridPos[0]-gridPos[2])/scaleTileSize) + safteyMargin
    renderHeight = math.floor((screen.get_height()-gridPos[1]-gridPos[3])/scaleTileSize) + safteyMargin
    gridWidth = tileGrid[0][0]
    gridHeight = tileGrid[0][1]
    gridLayers = tileGrid[depth+1]
    renderObjects = True
    for layer in range(len(gridLayers)-1):
        gridData = gridLayers[layer+1]
        tilePos = [origTilePos[0],origTilePos[1]]
        tileOffX = math.floor(camPos[0]/scaleTileSize)
        tileOffY = math.floor(camPos[1]/scaleTileSize)
        tileID = tileOffX
        tileID += tileOffY*gridWidth
        #tileID -=1
        gridRow = tileOffY
        for row in range(renderHeight):
            if renderObjects:
                renderAllObjectatRow(gridRow, depth)
            gridRow += 1
            for col in range(renderWidth):
                tileType = 0
                if tileID >= 0:
                    if tileID <= len(gridData)-1:
                        tileProperties = gridData[tileID][1]
                        tileDepth = depth
                        tileType = gridData[tileID][0]
                        renderTileType(tilePos, tileType, tileDepth, tileID)
                tilePos[0] += scaleTileSize
                tileID += 1
            tileID += gridWidth-renderWidth
            tilePos[0] = origTilePos[0]
            tilePos[1] += scaleTileSize

def getDepthId(depth):
    depths = tileGrid
    depthInsertion = len(depths)
    for i in range(len(depths)):
        if depths[i+1][0] == depth:
            return(i+1)
        if depths[i+1][0]+1 == depth:
            depthInsertion = i+1+1
    tileGrid.insert(depthInsertion,[depth])
    for layer in range(3):
        tileGrid[depthInsertion].append([])
        for i in range(tileGrid[0][0]):
            for i in range(tileGrid[0][1]):
                tileGrid[depthInsertion][layer+1].append([0,''])
    return depthInsertion

def movePlayer():
    global gridZoom
    tileIdx = getTileIndex(pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    # Basic Player Controls
    origZoom = gridZoom
    if keys[pygame.K_MINUS]:
        gridZoom -= 0.05
    if keys[pygame.K_EQUALS]:
        gridZoom += 0.05
    if gridZoom <= 0:
        gridZoom = 0.05
    if origZoom != gridZoom:
        loadSprites()
    if keys[pygame.K_w]:
        playerPos[1] -= 2
    if keys[pygame.K_s]:
        playerPos[1] += 2
    if keys[pygame.K_a]:
        playerPos[0] -= 2
    if keys[pygame.K_d]:
        playerPos[0] += 2
    camPos[0] = playerPos[0]*gridZoom - ((screen.get_width()-gridPos[0]-gridPos[2])/2)
    camPos[1] = playerPos[1]*gridZoom - ((screen.get_height()-gridPos[1]-gridPos[3])/2) - playerSurfs.get_height()/2
    #Basic Tile Brush Controls
    if keys[pygame.K_e]:
        depthID = getDepthId(tileBrush[3])
        tileBrush[0] = tileGrid[depthID][tileBrush[1]+1][tileIdx][0]
        tileBrush[2] = tileGrid[depthID][tileBrush[1]+1][tileIdx][1]
    if keys[pygame.K_r]:
        tileBrush[3] = 0
    if keys[pygame.K_t]:
        tileBrush[3] = 1
    if keys[pygame.K_y]:
        tileBrush[3] = 2
    if keys[pygame.K_1]:
        tileBrush[1] = 0
    if keys[pygame.K_2]:
        tileBrush[1] = 1
    if keys[pygame.K_3]:
        tileBrush[1] = 2
    lockCamera()

def lockCamera():
    #Locks the Camera to make sure it in within the Grid Width and Height
    if camPos[0] > (tileGrid[0][0]*scaleTileSize)-(screen.get_width()-gridPos[0]-gridPos[2]):
        camPos[0] = (tileGrid[0][0]*scaleTileSize)-(screen.get_width()-gridPos[0]-gridPos[2])
    if camPos[1] > (tileGrid[0][1]*scaleTileSize)-(screen.get_height()-gridPos[1]-gridPos[3]):
        camPos[1] = (tileGrid[0][1]*scaleTileSize)-(screen.get_height()-gridPos[1]-gridPos[3])
    if camPos[0] < 0:
        camPos[0] = 0
    if camPos[1] < 0:
        camPos[1] = 0 

def worldPosToScreenPos(Rect: pygame.Rect, Offset: tuple):
    return [Rect.x-gridPos[0]+Offset[0], Rect.y-gridPos[1]+Offset[1]]
    #[Rect.x-gridPos[0]+(playerSurfs.get_width()/2), Rect.y-gridPos[1]+playerSurfs.get_height()]

def getTileIndex(Pos: tuple):
    global scaleTileSize
    #Converts a Screen Position to a Tile Grid Index
    gridHeight = tileGrid[0][1]
    gridWidth = tileGrid[0][0]
    gridX = math.floor((Pos[0]+camPos[0]-gridPos[0])/scaleTileSize)
    gridY = math.floor((Pos[1]+camPos[1]-gridPos[1])/scaleTileSize)
    tileID = gridX+(gridY*gridWidth)
    return tileID

def renderPlayer():
    playerRect.x = (playerPos[0]*gridZoom - (playerSurfs.get_width()/2) - camPos[0] + gridPos[0])
    playerRect.y = (playerPos[1]*gridZoom - playerSurfs.get_height() - camPos[1] + gridPos[1])
    renderedObjects.append([playerSurfs, playerRect, playerPos, 1])

def tickLoop(clock: pygame.time.Clock):
    global tileBrush
    global playerSurfs
    global selectorTiles
    global playerRect
    global playerPos
    global renderedObjects
    global viewportSurfs 
    global viewportRects
    global globalFrame
    globalFrame += 1
    # Rendered Objects 
    renderedObjects = []
    # Renders all Depths
    movePlayer()
    renderPlayer()
    for i in range(len(tileGrid)-1):
        renderTiles(i)
        #pygame.display.update()
        #breakpoint()
    tileIdx = getTileIndex([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]])
    roundedCursor = [((math.floor((pygame.mouse.get_pos()[0]-gridPos[0] + (camPos[0]%scaleTileSize))/scaleTileSize))*scaleTileSize) + gridPos[0] - (camPos[0]%scaleTileSize) - (1*gridZoom)]
    roundedCursor.append(((math.floor((pygame.mouse.get_pos()[1]-gridPos[1]  + (camPos[1]%scaleTileSize))/scaleTileSize))*scaleTileSize) + gridPos[1] - (camPos[1]%scaleTileSize) - (1*gridZoom))
    screen.blit(selectorTiles[math.floor((globalFrame/30)%2)].main, roundedCursor)
    # Sets the hovered tile to the selected brush
    if pygame.mouse.get_pressed()[0]:
        if tileIdx >= 0:
            tileDepth = tileBrush[3]
            tileLayer = tileBrush[1]
            depthID = getDepthId(tileDepth)
            if tileIdx <= len(tileGrid[depthID][tileLayer+1])-1:
                tileProperties = [tileBrush[0],tileBrush[2]]
                tileGrid[depthID][tileLayer+1][tileIdx] = tileProperties
    for i in range(len(viewportRects)):
        screen.blit(viewportSurfs[i],viewportRects[i])
    gui.renderText(screen, 2, 0, f'Player Pos: {playerPos}, [{math.floor(playerPos[0]/tileSize)}, {math.floor(playerPos[1]/tileSize)}]', f'{fileRoot}Assets/Font/pixel.ttf', 16, (0,0,0))
    centeredRect = [playerRect.x-gridPos[0]+(playerSurfs.get_width()/2), playerRect.y-gridPos[1]+playerSurfs.get_height()]
    gui.renderText(screen, 2, 16, f'Player Rect: [{playerRect.x},{playerRect.y}], {centeredRect}, [{math.floor(centeredRect[0]/scaleTileSize)}, {math.floor(centeredRect[1]/scaleTileSize)}]', f'{fileRoot}Assets/Font/pixel.ttf', 16, (0,0,0))
    gui.renderText(screen, viewportSurfs[2].get_width()-2, 0, f'Zoom: {round(gridZoom*1000)/10}x', f'{fileRoot}Assets/Font/pixel.ttf', 16, (0,0,0), 'left')
    gui.renderText(screen, viewportSurfs[2].get_width()-2, 16, f'Brush: {tileBrush}', f'{fileRoot}Assets/Font/pixel.ttf', 16, (0,0,0), 'left')
    gui.renderText(screen, 2, screen.get_height()-24, f'FPS: {round(clock.get_fps())}', f'{fileRoot}Assets/Font/pixel.ttf', 20, (255,255,255))