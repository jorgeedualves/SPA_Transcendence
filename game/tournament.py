NUM_PLAYERS_TOURNAMENT = 4

class Tournament:
	def __init__(self):
		self.match = [0, 1]
		self.winners = [None, None]
		self.current_match = 1
		self.tour_winner = None
		self.over = False
		self.match_over = False

	def start_next_match(self):
		self.match_over = False
		if self.current_match == 2:
			self.match = [2, 3]
		if self.current_match == 3:
			self.match = [self.winners[0], self.winners[1]]

	def record_winner(self, winner_index):
		self.match_over = True
		if self.current_match == 1:
			self.winners[0] = self.match[winner_index]
		elif self.current_match == 2:
			self.winners[1] = self.match[winner_index]
		elif self.current_match == 3:
			self.tour_winner = self.match[winner_index]
			self.over = True
			return self.tour_winner
		self.current_match += 1

	def send_current_match(self):
		players = {
			'tourPlayer_1': self.match[0],
			'tourPlayer_2': self.match[1],
			'matchOver': self.match_over
		}
		return players
		
			