import random
import math

# set up
lanes = 5
cars = 1
t = .01  # seconds
data = [{'position': [1, random.random()*1000.], # e.g., [lane, pos]
		 'velocity': float(random.randint(22, 33)), # meters per second
	 	 'accel': 0. } # miles per hour per hour
		for car in range(cars)]
data = sorted(data, key=lambda x: x['position'][1])
print(data)
max_accel = .73
max_decel = 2.
delta = 4.
desired_vel = 33.
clearing_time = 1.5  #

# initial equilibria
for loop in range(15):
	for car in range(cars):
		print('iteration =', loop)
		print('car =', car)
		print('pos =', data[car]['position'][1])
		print('a =', data[car]['accel'])
		print('v =', data[car]['velocity'])
		print()

		v = data[car]['velocity']
		a = data[car]['accel']
		if v + a*t < 0:
			data[car]['position'][1] = (data[car]['position'][1] - (0.5 * (v**2) / a)) % 1000

			data[car]['velocity'] = 0
			v = data[car]['velocity']
		else:
			# calculate new positions        
			data[car]['position'][1] = (data[car]['position'][1] + v*t + 0.5*a*(t**2)) % 1000

			# update velocity
			data[car]['velocity'] = v + a*t
			v = data[car]['velocity']

		# update accel
		leading_car = (car + 1) % len(data)
		velocity_diff = v - data[leading_car]['velocity']
		position_diff = max(data[leading_car]['position'][1] - data[car]['position'][1], .02)
		s_star = max(0, clearing_time*v + (v*velocity_diff)/(2*math.sqrt(max_accel*max_decel)))
		term1 = v / desired_vel
		term2 = s_star / position_diff
		data[car]['accel'] = max(min(max_accel, max_accel*(1 - term1 - (term2)**2.)), -max_decel)

	new_order_data = sorted(data, key=lambda x: x['position'][1])
	if loop > 50 and new_order_data != data:
			print("failed")
	data = new_order_data

# choose which car is going to go slower
perturbation = random.choice(range(cars))

