from django.shortcuts import render

from .models import Article

def index(request):
    articles = Article.objects.all().order_by('-pub_date')  # newest first
    return render(request, 'news/index.html', {'articles': articles})