from django.shortcuts import render, redirect

def index(request):
    articles = [
        {'title': 'Dummy Article 1', 'author': 'Author A', 'content': 'Content A'},
        {'title': 'Dummy Article 2', 'author': 'Author B', 'content': 'Content B'},
    ]
    return render(request, 'news/home.html', {'articles': articles})

def add_post(request):
    if request.method == 'POST':
        # Just simulate adding a post
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        print("Received post:", title, author, content)
        return redirect('news-index')
    return render(request, 'news/add_article.html')