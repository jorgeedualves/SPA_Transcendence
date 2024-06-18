from .ball import Ball
from .player import Player
import asyncio
import time
from datetime import timedelta
from game.models import GameDB
import random
from django.utils import timezone

CAN_WIDTH = 1300
CAN_HEIGHT = 800
FPS = 60
WIN_GAME = 5

class Game:
	WIDTH = CAN_WIDTH
	HEIGHT = CAN_HEIGHT
	paused = False
	started = False
	ai = True
	last_ai_prediction = 0
	predicted_y = 0
	start_time = 0
	ended = False

def setup():
	global player_1, player_2, game, ball
	player_1 = Player(10, (CAN_HEIGHT / 2) - (Player.HEIGHT / 2))
	player_2 = Player(CAN_WIDTH - Player.WIDTH - 10, (CAN_HEIGHT / 2) - (Player.HEIGHT / 2))
	game = Game()
	ball = Ball(CAN_WIDTH / 2 - Ball.SIZE, CAN_HEIGHT / 2 - Ball.SIZE)

async def game_loop_logic(send_game_state):
	frame_duration = 1 / FPS
	next_frame_time = time.perf_counter() + frame_duration
	while game.started:
		if not game.paused:
			collision()
			player_1.move()
			if not game.ai:
				player_2.move()
			else:
				player_2.y_pos = ai_move(0.1, player_2.y_pos)

			ball.x_pos += ball.ball_speed * ball.ball_orientation[0]
			ball.y_pos += ball.ball_speed * ball.ball_orientation[1]

			if player_1.score == WIN_GAME or player_2.score == WIN_GAME:
				game.started = False
				game.ended = True
			game_state = get_game_data()
			await send_game_state(game_state)
		# Dormir pelo tempo restante do frame
		next_frame_time += frame_duration
		sleep_time = next_frame_time - time.perf_counter()
		if sleep_time > 0:
			await asyncio.sleep(sleep_time)
		else:
			next_frame_time = time.perf_counter() + frame_duration

async def start_game(send_game_state):
	game.started = True
	game.start_time = time.time()
	await game_loop_logic(send_game_state)

def collision():
	if (ball.x_pos >= player_1.x_pos
	and	ball.x_pos <= player_1.x_pos + Player.WIDTH
	and ball.y_pos >= player_1.y_pos 
	and ball.y_pos <= player_1.y_pos + Player.HEIGHT):
		ball.ball_orientation[0] = 1
		player_1.hits += 1

	if (ball.x_pos >= player_2.x_pos - 10
	and ball.x_pos <= player_2.x_pos + Player.WIDTH
	and ball.y_pos >= player_2.y_pos
	and ball.y_pos <= player_2.y_pos + Player.HEIGHT):
		ball.ball_orientation[0] = -1
		player_2.hits += 1

	if (ball.y_pos + ball.SIZE >= CAN_HEIGHT or ball.y_pos <= 0):
		ball.ball_orientation[1] *= -1

	if ball.x_pos + 10 > CAN_WIDTH:
		player_1.score += 1
		ball.reset()

	if ball.x_pos < 0:
		player_2.score += 1
		ball.reset()

def update_event(event: str, state: bool, send_game_state=None):
	if event == 'p1_up':
		player_1.go_up = state
	elif event == 'p1_down':
		player_1.go_down = state
	elif event == 'p2_up':
		player_2.go_up = state
	elif event == 'p2_down':
		player_2.go_down = state
	if event == 'isPaused':
		game.paused = state
	if event == 'game_started':
		if (send_game_state):
			asyncio.create_task(start_game(send_game_state))
	if (event == 'ai'):
		game.ai = state

def predict_ball():
	future_x = ball.x_pos
	future_y = ball.y_pos
	future_orientation_x = ball.ball_orientation[0]
	future_orientation_y = ball.ball_orientation[1]

	time_to_edge = (player_2.x_pos - future_x) / future_orientation_x

	game.predicted_y = future_y + future_orientation_y * time_to_edge

	return game.predicted_y

def ai_move(smoothing, paddle_y, error_margin=50):
	
	current_time = time.time()

	if ball.x_pos >= CAN_WIDTH / 2:
		if (current_time - game.last_ai_prediction >= 1):
			game.predicted_y = predict_ball()
			game.last_ai_prediction = current_time
	else:
		game.predicted_y = CAN_HEIGHT / 2

	target_y = game.predicted_y - Player.HEIGHT / 2
	target_y = max(0, min(CAN_HEIGHT - Player.HEIGHT, target_y))

	new_y = paddle_y + (target_y - paddle_y) * smoothing

	if (abs(new_y - paddle_y) > Player.vel):
		if (new_y > paddle_y and paddle_y + Player.HEIGHT < CAN_HEIGHT):
			paddle_y += Player.vel
		elif (new_y < paddle_y and paddle_y > 0):
			paddle_y -= Player.vel
	else:
		paddle_y = new_y

	return paddle_y

def save_db(user):
    end_time = time.time()
    duration = timedelta(microseconds=end_time - game.start_time)

    player2_name = "AI" if game.ai else "Guest"

    game_instance = GameDB(
        player1=user,
        player2=player2_name,
        score_player1=player_1.score,
        score_player2=player_2.score,
        hits_player1=player_1.hits,
        duration=duration,
        date=timezone.now()
    )
    game_instance.save()

def get_game_data():
	game_state = {
		'p1_y': player_1.y_pos,
		'p2_y': player_2.y_pos,
		'p1_score': player_1.score,
		'p2_score': player_2.score,
		'ball_x': ball.x_pos,
		'ball_y': ball.y_pos,
		'isPaused' : game.paused,
		'game_started': game.started,
		'game_ended': game.ended,
		'p1_hits': player_1.hits,
		'ai': game.ai,
		'start_time': game.start_time,
    }
	return game_state

def get_static_game_data():
	static_data = {
		'width': Game.WIDTH,
		'height': Game.HEIGHT,
		'p_width': Player.WIDTH,
		'p_height': Player.HEIGHT,
		'p1_x': player_1.x_pos,
		'p2_x': player_2.x_pos,
	}
	return static_data
