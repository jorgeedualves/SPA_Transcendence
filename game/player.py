CAN_HEIGHT = 648


class Player:
	WIDTH = 10
	HEIGHT = 80
	vel = 10
	go_up = False
	go_down = False
	alias = None

	def __init__(self, x_pos, y_pos):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.score = 0
		self.hits = 0

	def move(self):
		if self.go_up and self.y_pos > 0:
			self.y_pos -= self.vel
		if self.go_down and self.y_pos + self.HEIGHT < CAN_HEIGHT:
			self.y_pos += self.vel

	def reset(self, x_pos):
		self.y_pos = CAN_HEIGHT / 2 - self.HEIGHT / 2
		self.x_pos = x_pos
		self.score = 0
		self.hits = 0
