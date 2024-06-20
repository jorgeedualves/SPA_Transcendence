NUM_PLAYERS_TOURNAMENT = 4

class Tournament:
	def __init__(self):
		self.match = [0, 1]
		self.winners = [None, None]
		self.current_match = 1
		self.tour_winner = None
		self.over = False

	def start_next_match(self):
		if self.current_match == 1:
			return self.send_current_match()
		if self.current_match == 2:
			self.match = [2, 3]
			return self.send_current_match()
		if self.current_match == 3:
			self.match = [self.winners[0], self.winners[1]]
			return self.send_current_match()

	def record_winner(self, winner_index):
		if self.current_match == 1:
			self.winners[0] = self.match[winner_index]
		elif self.current_match == 2:
			self.winners[1] = self.match[winner_index]
		elif self.current_match == 3:
			self.tour_winner = self.match[winner_index]
			self.over = True
			return self.tour_winner
		self.current_match += 1
		self.start_next_match()

	def send_current_match(self):
		players = {
			'TourPlayer_1': self.match[0],
			'TourPlayer_2': self.match[1]
		}
		return players
		
			