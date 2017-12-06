import sys
import pygame
from test_sim import TestSim
from single_lane_idm import SingleLaneIDM
from multi_lane_idm import MultiLaneIDM
from lane_switch_idm import LaneSwitchIDM
from pygame.locals import *
from constants import *
from car import *

# set up screen and clock
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)
surface = pygame.Surface(screen.get_size()).convert()
surface = surface.convert()
surface.fill(BACKGROUND_COLOR)
clock = pygame.time.Clock()

def draw_lanes():
    """
    Draw the lane markings.
    """
    y = VERTICAL_MARGIN
    for i in range(LANES + 1):
        j = 0
        while j < SCREEN_WIDTH:
            # create and draw a rectangle for each lane hash
            r = pygame.Rect((j, y), LANE_HASH_DIMENSIONS)
            pygame.draw.rect(screen, LANE_COLOR, r)
            j += LANE_HASH_WIDTH + LANE_HASH_SPACING
        y += LANE_HEIGHT

if __name__ == "__main__" :

    # check usage: python main.py NameOfSimulation
    assert(len(sys.argv) > 1)
    assert(sys.argv[1] in SIMULATION_NAMES)

    # instatiate and initialize simulation
    sim = globals()[sys.argv[1]]()
    sim.initialize()

    while True:
        # quit on any key
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                pygame.quit()
                sys.exit()

        # update display
        draw_lanes()
        sim.draw(screen)
        sim.update()
        pygame.display.flip()
        pygame.display.update()
        screen.blit(surface, (0, 0))
        clock.tick(FPS)
