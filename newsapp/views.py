from django.shortcuts import render, redirect
from django.utils import timezone


from .models import Article

def index(request):
    articles = Article.objects.all().order_by('-pub_date')  # newest first
    return render(request, 'news/index.html', {'articles': articles})

def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')

        if title and author and content:
            Article.objects.create(
                title=title,
                author=author,
                content=content,
                pub_date=timezone.now()
            )
            return redirect('news-index')  

    return render(request, 'news/add_post.html')