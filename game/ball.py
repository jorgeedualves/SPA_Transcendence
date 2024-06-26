import random
import math

CAN_WIDTH = 1053
CAN_HEIGHT = 648

class Ball:
	SIZE = 20
	ball_speed = 6
	ball_orientation = [math.pow(2, math.floor(random.random() * 2)+1)- 3, 
						math.pow(2, math.floor(random.random() * 2)+1)- 3]

	def __init__(self, x_pos, y_pos):
		self.x_pos = x_pos
		self.y_pos = y_pos
	
	def reset(self):
		self.ball_orientation = [math.pow(2, math.floor(random.random() * 2)+1)- 3, 
								math.pow(2, math.floor(random.random() * 2)+1)- 3]
		self.x_pos = CAN_WIDTH / 2 - Ball.SIZE
		self.y_pos = CAN_HEIGHT / 2 - Ball.SIZE
