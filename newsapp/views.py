from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Category
from .forms import ArticleForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from .tokens import account_activation_token

WEATHER_API_KEY = "9892810cb987a16f049b84f8193326ce"

WEATHER_API_KEY = "9892810cb987a16f049b84f8193326ce"
CITIES = ["Cape Town", "Johannesburg", "Durban", "Pretoria", "Bloemfontein"]


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        return {
            "city": city,
            "temp": response["main"]["temp"],
            "description": response["weather"][0]["description"].title(),
            "icon": response["weather"][0]["icon"],
            "main": response["weather"][0]["main"]  # e.g., Rain, Clear
        }
    except:
        return None

def home(request):
    articles = Article.objects.all().order_by("-created_at")
    weather_data = [get_weather(city) for city in CITIES]
    return render(request, "newsapp/home.html", {
        "articles": articles,
        "weather_list": weather_data
    })

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'newsapp/article_detail.html', {"article": article})

@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article added successfully!")
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'newsapp/add_article.html', {"form": form})

def categories(request):
    cats = Category.objects.all()
    return render(request, 'newsapp/categories.html', {"categories": cats})

def category_articles(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    articles = Article.objects.filter(category=category).order_by('-created_at')
    return render(request, 'newsapp/category_articles.html', {
        "category": category,
        "articles": articles
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'newsapp/login.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user without disabling the account
            user.is_active = True  # Make sure the user is active immediately
            user.save()

            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You are now logged in.")
            return redirect('home')  # Redirect to the home page or wherever you want
    else:
        form = RegisterForm()

    return render(request, "newsapp/register.html", {"form": form})

@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated! You are now logged in.")
        return redirect('add_article')
    else:
        return HttpResponse('Activation link is invalid or expired!')

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # Ensure the logged-in user is the author of the article
    if article.author != request.user:
        messages.error(request, "You are not authorized to edit this article.")
        return redirect('article_detail', article_id=article.id)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'newsapp/edit_article.html', {'form': form, 'article': article})

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # Ensure the logged-in user is the author of the article
    if article.author != request.user:
        messages.error(request, "You are not authorized to delete this article.")
        return redirect('article_detail', article_id=article.id)

    article.delete()
    messages.success(request, "Article deleted successfully!")
    return redirect('home')  # Redir
