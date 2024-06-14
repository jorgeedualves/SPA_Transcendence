CAN_HEIGHT = 800


class Player:
	WIDTH = 10
	HEIGHT = 100
	vel = 10
	go_up = False
	go_down = False

	def __init__(self, x_pos, y_pos):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.score = 0

	def move(self):
		if self.go_up and self.y_pos > 0:
			self.y_pos -= self.vel
		if self.go_down and self.y_pos + self.HEIGHT < CAN_HEIGHT:
		    self.y_pos += self.vel
