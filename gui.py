import pygame
global textCache
textCache = {}

def renderText(screen: pygame.Surface, x: int, y: int, text: str, font: str, fontSize: int, fontColor: pygame.Color, alignment: str = 'None'):
    global textCache
    loadedFont = pygame.font.Font(font, fontSize)
    textLines = text.split('\n')
    OffX = 0
    OffY = 0
    
    for i in range(len(textLines)):
        cacheKey = (textLines[i], font, fontSize, fontColor)
        if cacheKey in textCache:
                textSurf = textCache[cacheKey]
        else:
            textSurf = loadedFont.render(textLines[i], False, fontColor)
            textCache[cacheKey] = textSurf
        if alignment.lower() == 'center':
            OffX = textSurf.get_width()/-2
            OffY = textSurf.get_height()/-2
        elif alignment.lower() == 'left':
            OffX = textSurf.get_width()*-1
        screen.blit(textSurf, (x+OffX, y+OffY + i * (loadedFont.get_height() + 1)))