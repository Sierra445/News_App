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
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            
            current_site = get_current_site(request)
            subject = 'Activate Your Newsly Account'
            message = render_to_string('newsapp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(
                subject,
                message,
                'no-reply@newsly.com',  
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Account created! Please check your email to activate your account.')
            return redirect('login')  
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
