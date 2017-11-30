import pygame
from pygame.locals import *
from constants import *

class Car(object):

    def __init__(self, pos):
        """
        Create a car at a position. Pos is an ordered pair.
        """
        self.color = CAR_COLOR
        self.pos = pos

    def draw(self, surface):
        """
        Draw car at its current position.
        """
        r = pygame.Rect(self.pos, CAR_DIMENSIONS)
        pygame.draw.rect(surface, self.color, r)
