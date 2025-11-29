from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.utils import timezone, translation
from django.utils.translation import gettext as _
from django.http import JsonResponse  # ADDED

import requests
import os


from .models import Article, Post

def index(request):
    # show articles as stored; UI translations come from .po/.mo files
    articles = Article.objects.all().order_by('-pub_date')
    title = _("Latest News")
    return render(request, 'news/index.html', {'articles': articles, 'title': title})

def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        category = request.POST.get('category')  # optional

        if title and content:
            Post.objects.create(
                title=title,
                author=author,
                content=content,
                pub_date=timezone.now()
            )
            # also create Article for news listing (optional)
            Article.objects.create(
                title=title,
                content=content,
                author=author,
                pub_date=timezone.now(),
                category=category or ""
            )
            return redirect(reverse('news:index'))  # CHANGED: use named URL in news app

    return render(request, 'news/add_post.html')

def categories(request):
    selected = request.GET.get('category')
    qs = Article.objects.all().order_by('-pub_date')

    field_names = [f.name for f in Article._meta.get_fields() if hasattr(f, 'name')]
    if 'category' in field_names:
        if selected:
            qs = qs.filter(category__iexact=selected)
        categories = Article.objects.values_list('category', flat=True).distinct()
    else:
        selected = None
        categories = []

    return render(request, 'news/categories.html', {
        'articles': qs,
        'categories': categories,
        'selected': selected,
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.POST.get('next') or reverse('news:index'))
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form, 'next': request.GET.get('next', '')})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('news:index'))
    else:
        form = UserCreationForm()
    return render(request, 'news/signup.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect(reverse('news:index'))

def set_language(request):
    lang = request.GET.get('language')
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER', reverse('news:index'))
    if lang and lang in dict(settings.LANGUAGES):
        # set session key and cookie
        request.session['django_language'] = lang
        translation.activate(lang)
        response = redirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
    return redirect(next_url)

def weather_api(request):
    q = request.GET.get('q')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not q and not (lat and lon):
        return JsonResponse({'error': 'Provide q=city or lat & lon'}, status=400)

    api_key = getattr(settings, 'WEATHER_API_KEY', None) or getattr(settings, 'OPENWEATHER_API_KEY', None)
    if not api_key:
        return JsonResponse({'error': 'Weather API key not configured'}, status=500)

    params = {'appid': api_key, 'units': 'metric'}
    if q:
        params['q'] = q
    else:
        params.update({'lat': lat, 'lon': lon})

    url = 'https://api.openweathermap.org/data/2.5/weather'
    try:
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch weather', 'details': str(e)}, status=502)

    result = {
        'name': data.get('name'),
        'weather': data.get('weather'),
        'main': data.get('main'),
        'wind': data.get('wind'),
    }
    return JsonResponse(result)