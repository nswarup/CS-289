"""
Simulation of the intelligent driver model on multiple lanes with switching.
"""

import random
import math
from simulation import Simulation
from car import Car
from constants import *

NUM_CARS = 30
MAX_ACCEL = .73
MAX_DECCEL = 2.
DELTA = 4.
DESIRED_VEL = 40.
CLEARING_TIME = 1.5
TIME_STEP = 0.2 # seconds
LANE_CHANGE_VEL_DISCOUNT = .8
RADIUS_OBSERVED = 50

class LaneSwitchIDM(Simulation):

    def initialize(self):
        # constants
        self.cars = [Car(pos=random.random()*SCREEN_WIDTH,
                            lane=random.randint(0, LANES - 1),
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

            options = {'down_vel': 0.0, 'up_vel': 0.0}

            # staying in the same lane
            if v + a*TIME_STEP < 0:
                # edge case to make sure you don't go backwards
                options['same_pos'] = (car.pos - (0.5 * (v**2) / a))
                options['same_vel'] = 0

            else:
                # calculate new positions
                options['same_pos'] = (car.pos + v*TIME_STEP + 0.5*a*(TIME_STEP**2))
                # update velocity
                options['same_vel'] = v + a*TIME_STEP

            # changing up
            if car.lane > 0:
                new_lane = car.lane - 1
                density = 0
                average_velocity = 0
                for other_car in self.cars:
                    if other_car.lane == new_lane and abs(other_car.pos - car.pos) <= 50:
                        density += 1
                        average_velocity += other_car.vel
                if density:
                    average_velocity /= density
                else:
                    average_velocity = DESIRED_VEL
                # TODO: slow it down if the car changes lanes and make the position reflect that the car would be moving at an angle
                options['up_vel'] = average_velocity * LANE_CHANGE_VEL_DISCOUNT
            options['up_pos'] = options['same_pos']

            # changing down
            if car.lane < LANES - 1:
                new_lane = car.lane + 1
                density = 0
                average_velocity = 0
                for other_car in self.cars:
                    if other_car.lane == new_lane and abs(other_car.pos - car.pos) <= 50:
                        density += 1
                        average_velocity += other_car.vel
                if density:
                    average_velocity /= density
                else:
                    average_velocity = DESIRED_VEL
                # TODO: slow it down if the car changes lanes and make the position reflect that the car would be moving at an angle
                options['down_vel'] = average_velocity * LANE_CHANGE_VEL_DISCOUNT
            options['down_pos'] = options['same_pos']

            if options['up_vel'] > options['down_vel'] and options['up_vel'] > options['same_vel']:
                car.change_lane(UP)
                car.vel = options['up_vel']
            elif options['down_vel'] > options['same_vel']:
                car.change_lane(DOWN)
                car.vel = options['down_vel']

            car.pos = options['same_pos']
            v = car.vel

            # make a decision



            # update accel
            leading_car = None
            for other_car_index in range(car_index+1, car_index+NUM_CARS):
                other_car = self.cars[other_car_index % NUM_CARS]
                if other_car.lane == car.lane:
                    leading_index = other_car_index % NUM_CARS
                    leading_car = self.cars[leading_index]
                    break

            term1 = v / DESIRED_VEL
            term2 = 0
            if leading_car:
                velocity_diff = v - leading_car.vel
                position_diff = leading_car.pos - car.pos

                if leading_car.pos - car.pos < 0:
                    position_diff = SCREEN_WIDTH + leading_car.pos - car.pos

                # track average following distance
                car.av_following_dist += float(position_diff) / SAMPLE_POINT

                s_star = max(0, CLEARING_TIME*v + (v*velocity_diff)/(2*math.sqrt(MAX_ACCEL*MAX_DECCEL)))
                term2 = s_star / position_diff
            else:
                raise RuntimeError("No leading car found")
            car.accel = max(min(MAX_ACCEL, MAX_ACCEL*(1 - term1 - (term2)**2.)), -MAX_DECCEL)

            # handle lap counting
            handle_laps(car)

        self.cars = sorted(self.cars, key=lambda x: x.pos)
