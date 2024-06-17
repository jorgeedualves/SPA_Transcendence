from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import translation

from django.shortcuts import render
from django.utils import translation

@ensure_csrf_cookie
def account(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    
    user = request.user
    profile_picture_url = user.profile_picture_url if user.profile_picture_url else 'static/images/default_picture.png'
    context = {
        'profile_picture_url': profile_picture_url,
    }
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html', context)
    return render(request, 'index.html', context)