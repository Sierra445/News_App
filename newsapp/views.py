from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Category
from .forms import ArticleForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.contrib import messages

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
            return redirect('home')

        # If authentication fails
        messages.error(request, "Invalid username or password. If you don't have an account, please sign up first.")

    return render(request, 'newsapp/login.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # save the new user

            # Automatically log in the user
            login(request, user)

            # Add a success message
            messages.success(request, f"Account created! Welcome, {user.username}.")

            # Redirect directly to add article page
            return redirect('add_article')
        else:
            # Add error message if form is invalid
            messages.error(request, "There was an error creating your account. Please check the details.")

    else:
        form = RegisterForm()

    return render(request, 'newsapp/register.html', {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('home')
