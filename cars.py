import random
import math

# set up
lanes = 5
cars = 30
t = .1  # seconds
data = [{'position': [1, random.random()], 
		 'velocity': float(random.randint(22, 33)), # meters per second
		 'accel': 0. } # miles per hour per hour
		for car in range(cars)]
data = sorted(data, key=lambda x: x['position']) 
max_accel = 4.
max_deaccel = 2.5
delta = 1.
desired_vel = 33.
clearing_time = t / 0.55

# initial equilibria
for loop in range(10000):
	for car in range(cars):
		# calculate new positions
		v = data[car]['velocity']
		a = data[car]['accel']
		data[car]['position'][1] = (data[car]['position'][1] + v*t + (0.5*a*t)**2) % 1

		# update velocity
		data[car]['velocity'] = v + a*t
		v = data[car]['velocity']

		# update accel
		leading_car = car + 1 if car + 1 != len(data) else 0
		velocity_diff = v - data[leading_car]['velocity']
		position_diff = max(data[car]['position'][1] - data[leading_car]['position'][1], .02)
		s_star = clearing_time*v + (v*velocity_diff)/(2*math.sqrt(max_accel*max_deaccel))
		term1 = v / desired_vel
		term2 = s_star / position_diff
		data[car]['accel'] = max_accel*(1 - term1 - (term2)**2.)

	new_order_data = sorted(data, key=lambda x: x['position']) 
	if loop > 50 and new_order_data != data:
		print("failed")

# choose which car is going to go slower
perterbation = random.choice(range(cars))

