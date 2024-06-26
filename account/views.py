from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import translation
from django.db.models import F, Avg, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from game.models import GameDB
import pytz
from django.utils.timezone import localtime

@login_required
@ensure_csrf_cookie
def account(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    
    user = request.user
    profile_picture_url = user.profile_picture_url if user.profile_picture_url else '/static/images/default_picture.png'
    
    target_timezone = pytz.timezone('America/Sao_Paulo')

    games = GameDB.objects.filter(player1=user).order_by('-date')  # Order by date descending
    game_data = [{
        'date': localtime(game.date, target_timezone).strftime('%H:%M %d/%m/%Y'),  # Format the date as DD/MM/YYYY
        'player1': game.player1.username,
        'player2': game.player2,
        'score_player1': game.score_player1,
        'score_player2': game.score_player2,
        'hits_player1': game.hits_player1,
        'duration': game.duration.total_seconds()
    } for game in games]
    
    total_games = games.count()
    games_against_ai = games.filter(player2='AI').count()
    games_against_others = total_games - games_against_ai
    
    total_duration = games.aggregate(Sum('duration'))['duration__sum'] or 0
    total_points = games.aggregate(Sum('score_player1'))['score_player1__sum'] or 0

    average_time_to_point = (total_duration.total_seconds() / total_points) if total_points > 0 else 0
	
    statistics = {
        'total_games': total_games,
        'victories': games.filter(score_player1__gt=F('score_player2')).count(),
        'losses': games.filter(score_player1__lt=F('score_player2')).count(),
        'win_rate': (games.filter(score_player1__gt=F('score_player2')).count() / total_games * 100) if total_games > 0 else 0,
        'average_duration': games.aggregate(Avg('duration'))['duration__avg'].total_seconds() if total_games > 0 else 0,
        'average_hits': games.aggregate(Avg('hits_player1'))['hits_player1__avg'] if total_games > 0 else 0,
        'average_time_to_point': average_time_to_point,
        'games_against_ai': (games_against_ai / total_games * 100) if total_games > 0 else 0,
        'games_against_others': (games_against_others / total_games * 100) if total_games > 0 else 0,
    }
    context = {
        'profile_picture_url': profile_picture_url,
        'games': game_data,
        'statistics': statistics,
        'language': language
    }

    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html', context)
    return render(request, 'index.html', context)