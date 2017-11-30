"""
Abstract base class for simulations. Defines required methods.
"""

from abc import ABCMeta, abstractmethod

class Simulation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self):
        """
        Do any necessary prep work.
        """

    @abstractmethod
    def draw(self, screen):
        """
        Draw cars. To be called at each time step.
        """
    @abstractmethod
    def update(self):
        """
        Update necessary car positions. To be called at each time step.
        """


