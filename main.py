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
fileRoot = ""

def Loop():
    gameLoop.tickLoop()
    screen.fill((2, 2, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(max_fps)

while True:
    Loop()