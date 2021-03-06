"""
Simulation of the intelligent driver model on a single lane.
"""

import random
import math
from simulation import Simulation
from car import Car
from constants import *

NUM_CARS = 2
MAX_ACCEL = .73
MAX_DECCEL = 2.
DELTA = 4.
DESIRED_VEL = 40.
CLEARING_TIME = 1.5
TIME_STEP = 0.5 # seconds

class SingleLaneIDM(Simulation):

    def initialize(self):
        # constants
        self.cars = [Car(pos=random.random() * SCREEN_WIDTH,
                            lane=0,
                            velocity=float(random.randint(22, 33)))
                    for i in range(NUM_CARS)]
        self.cars = sorted(self.cars, key=lambda x: x.pos)

    def draw(self, screen):
        for car in self.cars:
            car.draw(screen)

    def update(self):

        for car_index in range(NUM_CARS):
            car = self.cars[car_index]
            v = car.vel
            a = car.accel
            if v + a*TIME_STEP < 0:
                # edge case to make sure you don't go backwards
                car.pos = (car.pos - (0.5 * (v**2) / a))
                car.vel = 0
            else:
                # calculate new positions
                car.pos = (car.pos + v*TIME_STEP + 0.5*a*(TIME_STEP**2))

                # update velocity
                car.vel = v + a*TIME_STEP
            v = car.vel

            # wrap around screen if necessary, and update lap counter
            handle_laps(car)

            # update accel
            leading_index = (car_index + 1) % NUM_CARS
            leading_car = self.cars[leading_index]
            velocity_diff = v - leading_car.vel
            position_diff = leading_car.pos - car.pos

            if leading_car.pos - car.pos < 0:
                position_diff = SCREEN_WIDTH + leading_car.pos - car.pos
            s_star = max(0, CLEARING_TIME*v + (v*velocity_diff)/(2*math.sqrt(MAX_ACCEL*MAX_DECCEL)))

            # update running averages
            car.av_following_dist += float(position_diff) / SAMPLE_POINT

            term1 = v / DESIRED_VEL
            term2 = s_star / position_diff
            car.accel = max(min(MAX_ACCEL, MAX_ACCEL*(1 - term1 - (term2)**2.)), -MAX_DECCEL)

        self.cars = sorted(self.cars, key=lambda x: x.pos)
