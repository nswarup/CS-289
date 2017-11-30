"""
Simple simulator to test visualization. Shifts lanes downward until failure.
"""

from simulation import Simulation
from car import Car
from constants import *

class TestSim(Simulation):

    def initialize(self):
        self.car = Car(0, 0)
        self.iteration = 0

    def draw(self, screen):
        self.car.draw(screen)

    def update(self):
        self.car.pos += 5
        self.iteration += 1
        if self.iteration % 12 == 0:
            self.car.change_lane(DOWN)

