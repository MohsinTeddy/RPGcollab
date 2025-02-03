import pygame
import gameLoop
from sys import exit

screenWidth = 480
screenHeight = 360
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.init()
max_fps = 60
pygame.display.set_caption("RPG Collab")
clock = pygame.time.Clock()
fileRoot = "" # Mujtaba File Root
fileRoot = "C:/Mohsin/Coding/Python/RPG/" # Mohsin File Root
fileRoot = "" # No Root will search in current directory
# Since we need to have a path from the Root when using PyInstaller
# We can set it from here since we have different roots

gameLoop.initLoop(screen, fileRoot)

def Loop():
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()
    gameLoop.tickLoop()
    pygame.display.update()
    clock.tick(max_fps)

while True:
    Loop()