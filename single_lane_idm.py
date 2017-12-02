"""
Simulation of the intelligent driver model on a single lane.
"""

from simulation import Simulation

NUM_CARS = 10
MAX_ACCEL = .73
MAX_DECCEL = 2.
DELTA = 4.
DESIRED_VEL = 33.
CLEARING_TIME = 1.5  
TIME_STEP = 0.1 # seconds

class SingleLaneIDM(Simulation):

	def initialize(self):
			# constants
		 self.cars = [Car(position=random.random()*1000., 
							lane=0, 
							velocity=float(random.randint(22, 33))) 
					for i in range(NUM_CARS)]
		 self.cars = sorted(self.cars, key=lambda x: x.pos)


	def draw(self, screen):
		

	def update(self):
		

