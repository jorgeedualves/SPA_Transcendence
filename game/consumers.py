# consumers.py

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import (
	get_game_data, 
	get_static_game_data, 
	game_loop_logic,
	update_event,
	setup,
)

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user = self.scope['user']
		print(self.user)
		if self.user.is_anonymous:
			await self.close()
			return
		await self.accept()
		setup(self.user)

		static_game_data = get_static_game_data()
		await self.send(text_data=json.dumps({"static_data": static_game_data}))

		initial_state = get_game_data()
		await self.send(text_data=json.dumps({"game_state": initial_state}))
		self.game_task = None

	async def disconnect(self, close_code):
		if self.game_task:
			self.game_task.cancel()

	async def receive(self, text_data):
		data = json.loads(text_data)
		event = data.get('event')
		state = data.get('state')

		if event == 'game_started' or event == 'IsPaused' or event == 'ai' or event == 'guest':
			update_event(event, state, self.send_game_state)
		else:
			update_event(event, state)

	async def game_loop(self):
		await game_loop_logic(self.send_game_state)

	async def send_game_state(self, game_state):
		await self.send(text_data=json.dumps({"game_state": game_state}))