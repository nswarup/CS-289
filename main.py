import sys
import csv
import pygame
from os import system
from single_lane_idm import SingleLaneIDM
from multi_lane_idm import MultiLaneIDM
from lane_switch_idm import LaneSwitchIDM
from pygame.locals import *
from constants import *
from car import *

# set up screen and clock
screen = surface = None
if VISUALIZING:
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

def check_collisions(sim):
    """
    Check whether any cars have crashed.
    Note: assumes the simulation has a `cars` instance variable.
    """
    for i in range(len(sim.cars)):
        for j in range(i + 1, len(sim.cars)):
            if (sim.cars[i].lane == sim.cars[j].lane and
                    sim.cars[i].pos == sim.cars[j].pos):
                raise RuntimeError("Car crash!")

if __name__ == "__main__" :

    # check usage: python main.py NameOfSimulation [outfilename.csv]
    assert(len(sys.argv) > 1)
    assert(sys.argv[1] in SIMULATION_NAMES)

    # get name of outfile, if any
    outfile = sys.argv[2] if len(sys.argv) > 2 else 'out.csv'

    # instatiate and initialize simulation
    sim = globals()[sys.argv[1]]()
    sim.initialize()

    step = 0
    while True:

        # stop to collect data
        if step == SAMPLE_POINT:
            with open(outfile, 'w') as f:
                # fields to keep track of
                fields = [
                    'car_id',
                    'laps',
                    'av_following_dist',
                    'min_steps_per_lap',
                    'max_steps_per_lap',
                ]
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for car in sim.cars:
                    data = {
                        'car_id': id(car) % ID_SPACE,
                        'laps': car.lap,
                        'av_following_dist': round(car.av_following_dist, 2),
                        'min_steps_per_lap': car.min_steps,
                        'max_steps_per_lap': car.max_steps,
                    }
                    writer.writerow(data)
            print '\ncollected data at step ' + str(SAMPLE_POINT) + ' in ' + outfile + ':\n'
            system('cat ' + outfile + ' | column -t -s,') # pretty-print csv
            break

        if VISUALIZING:
            clock.tick(FPS)

            # quit on any key
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN:
                    pygame.quit()
                    sys.exit()

            # update display
            draw_lanes()
            sim.draw(screen)
            pygame.display.flip()
            pygame.display.update()
            screen.blit(surface, (0, 0))

        if CHECKING_COLLISIONS:
            check_collisions(sim)
        sim.update()
        for car in sim.cars:
            car.lap_step += 1
        step += 1
