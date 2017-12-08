"""
Simulation of the intelligent driver model on multiple lanes with switching. There is a single stopped car.
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
TIME_STEP = 0.5 # seconds

LANE_CHANGE_DISCOUNT = .9
RADIUS_OBSERVED = 100
STEPS_BETWEEN_SWITCH = 10

class SinglePerturbation(Simulation):

    def initialize(self):
        # constants
        self.cars = [Car(pos=random.random()*SCREEN_WIDTH,
                            lane=random.randint(0, LANES - 2),
                            velocity=float(random.randint(22, 33)))
                    for i in range(NUM_CARS)]
        self.cars[0].vel = 0
        self.cars[0].stopped = True
        self.cars[0].color = (0, 230, 0)
        self.cars = sorted(self.cars, key=lambda x: x.pos)

    def draw(self, screen):
        for car in self.cars:
            car.draw(screen)

    def update(self):
        def count_lane_density(car_index, new_lane, car):
            density = 0
            average_velocity = 0
            for other_car_index in range(car_index+1, car_index+NUM_CARS):
                other_car = self.cars[other_car_index % NUM_CARS]
                if other_car.lane == new_lane:
                    if abs(other_car.pos - car.pos) <= RADIUS_OBSERVED or abs(other_car.pos + 1000 - car.pos) <= RADIUS_OBSERVED:
                        density += 1
                        average_velocity += other_car.vel
            if density:
                average_velocity /= density
            else:
                average_velocity = DESIRED_VEL * .95
            return average_velocity
        
        for car_index in range(NUM_CARS):
            car = self.cars[car_index]
            if not car.stopped:
                v = car.vel
                a = car.accel
                up_vel = 0
                down_vel = 0

                if v + a*TIME_STEP < 0:
                    # edge case to make sure you don't go backwards
                    new_pos = (car.pos - (0.5 * (v**2) / a))
                    new_vel = 0
                else:
                    # calculate new positions
                    new_pos = (car.pos + v*TIME_STEP + 0.5*a*(TIME_STEP**2))

                    # update velocity
                    new_vel = v + a*TIME_STEP

                if car.last_switch > STEPS_BETWEEN_SWITCH:
                    # changing up
                    if car.lane > 0:
                        new_lane = car.lane - 1
                        up_vel = count_lane_density(car_index, new_lane, car) * LANE_CHANGE_DISCOUNT

                    # changing down
                    if car.lane < LANES - 1:
                        new_lane = car.lane + 1
                        down_vel = count_lane_density(car_index, new_lane, car) * LANE_CHANGE_DISCOUNT

                car.pos = new_pos
                car.vel = new_vel

                if up_vel > down_vel and up_vel > new_vel:
                    car.change_lane(UP)
                    car.vel *= LANE_CHANGE_DISCOUNT
                    car.last_switch = 0
                elif down_vel > new_vel:
                    car.change_lane(DOWN)
                    car.vel *= LANE_CHANGE_DISCOUNT
                    car.last_switch = 0
                v = car.vel            
                car.last_switch += 1


                # wrap around screen if necessary, and update lap counter
                handle_laps(car)

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
                    s_star = max(0, CLEARING_TIME*v + (v*velocity_diff)/(2*math.sqrt(MAX_ACCEL*MAX_DECCEL)))

                    # keep track of running average of following distance
                    car.av_following_dist += float(position_diff) / SAMPLE_POINT

                    term2 = s_star / position_diff
                    if position_diff < SCREEN_WIDTH / 100:
                        car.last_switch = STEPS_BETWEEN_SWITCH

                car.accel = max(min(MAX_ACCEL, MAX_ACCEL*(1 - term1 - (term2)**2.)), -MAX_DECCEL)

            self.cars = sorted(self.cars, key=lambda x: x.pos)