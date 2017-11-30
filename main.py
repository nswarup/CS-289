import pygame
from pygame.locals import *
from constants import *
from car import *

# set up screen and clock
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)
surface = pygame.Surface(screen.get_size()).convert() # may not need this
surface = surface.convert()
surface.fill(BACKGROUND_COLOR)
clock = pygame.time.Clock()

if __name__ == "__main__" :
    init_pos = (0, 200)
    car = Car(init_pos)
    while True:
        car.draw(screen)
        car.pos = (car.pos[0] + 5, car.pos[1])
        pygame.display.flip()
        pygame.display.update()
        screen.blit(surface, (0, 0))
        clock.tick(FPS)
