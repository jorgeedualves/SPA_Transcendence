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
    save_db
)

import time
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
player_1_score= 0 
player_2_score = 0
player_1_hits = 0 
ai = True

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        setup()

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

        if event == 'game_started':
            user_id = data.get('user_id')
            self.user = await self.get_user(user_id)
            update_event(event, state, self.send_game_state)
        elif event == 'isPaused' or event == 'ai' or event == 'guest':
            update_event(event, state, self.send_game_state)
        else:
            update_event(event, state)

    async def disconnect(self, close_code):
        if self.game_task:
            self.game_task.cancel()

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    async def game_loop(self):
        await game_loop_logic(self.send_game_state)

    async def send_game_state(self, game_state):
        if game_state.get('game_ended'):
            if self.user:
                await database_sync_to_async(save_db)(self.user)
        await self.send(text_data=json.dumps({"game_state": game_state}))