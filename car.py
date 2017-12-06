import pygame
from pygame.locals import *
from constants import *

def get_ypos(lane):
    """
    Helper to calculate the y coordinate of a car in a given lane.
    """
    return (VERTICAL_MARGIN + LANE_HEIGHT * lane
            + LANE_HEIGHT / 2 - CAR_HEIGHT / 2)

class Car(object):

    def __init__(self, pos, lane, velocity=0):
        """
        Create a car at position pos (on the x axis) in a given lane.
        """
        self.pos = pos
        self.lane = lane
        self.ypos = get_ypos(lane)
        self.color = CAR_COLOR
        self.vel = velocity
        self.accel = 0
        self.lap = 0

    def change_lane(self, direction):
        """
        Change to a new lane above or below.
        """
        new_lane = None
        if direction == UP:
            assert(self.lane - 1 >= 0)
            new_lane = self.lane - 1
        elif direction == DOWN:
            assert(self.lane + 1 < LANES)
            new_lane = self.lane + 1
        else:
            raise TypeError("Lane change direction must be UP or DOWN")
        self.lane = new_lane % LANES
        self.ypos = get_ypos(new_lane % LANES)

    def draw(self, screen):
        """
        Draw car at its current position, wrapping around if necessary.
        """
        r = pygame.Rect((self.pos, self.ypos), CAR_DIMENSIONS)
        pygame.draw.rect(screen, self.color, r)
