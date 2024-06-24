# consumers.py

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import (
	get_game_data, 
	get_static_game_data, 
	save_db,
	start_game,
	player_1,
	player_2,
	game,
	tournament
)

import time
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()

		static_game_data = get_static_game_data()
		await self.send(text_data=json.dumps({"static_data": static_game_data}))

		initial_state = get_game_data()
		await self.send(text_data=json.dumps({"game_state": initial_state}))
		self.game_task = None
		self.user = None

	async def receive(self, text_data):
		data = json.loads(text_data)
		event = data.get('event')
		state = data.get('state')

		if event in {'game_started'}:
			asyncio.create_task(start_game(self.send_game_state))
		elif event in {'user_id'}:
			user_id = data.get('user_id')
			self.user = await self.get_user(user_id)
		elif event in {'isPaused', 'ai', 'guest', 'tournament', 'restart'}:
			await self.update_event(event, state)
		else:
			self.update_key(event, state)

	async def disconnect(self, close_code):
		if self.game_task:
			self.game_task.cancel()

	@database_sync_to_async
	def get_user(self, user_id):
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			return None

	async def send_game_state(self, game_state, state_name=None):
		if game_state.get('game_ended'):
			if self.user:
				await database_sync_to_async(save_db)(self.user)
		if state_name:
			await self.send(text_data=json.dumps({state_name: game_state}))
		else:
			await self.send(text_data=json.dumps({"game_state": game_state}))
	
	def update_key(self, event: str, state):
		if event == 'p1_up':
			player_1.go_up = state
		elif event == 'p1_down':
			player_1.go_down = state
		elif event == 'p2_up':
			player_2.go_up = state
		elif event == 'p2_down':
			player_2.go_down = state

	async def update_event(self, event: str, state):
		if event == 'isPaused':
			game.paused = state
			await self.send_game_state(get_game_data())
		elif (event == 'ai'):
			game.ai = state
			await self.send_game_state(get_game_data())
		elif (event == 'guest'):
			player_2.alias = state
			await self.send_game_state(get_game_data())
		elif (event == 'tournament'):
			game.tournament = state
			if (state == True):
				game.ai = False
				tournament.reset()
				await self.send(text_data=json.dumps({"game_tour": tournament.send_current_match()}))
				await self.send_game_state(get_game_data())
		elif (event == 'restart'):
			game.reset(game.tournament, game.ai)
			await self.send_game_state(get_game_data())
			await self.send(text_data=json.dumps({"game_restart": True}))
