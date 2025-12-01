from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Temporary: Use Django's built-in views for auth
urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('add-article/', views.add_article, name='add_article'),
    path('categories/', views.categories, name='categories'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('category/<int:category_id>/', views.category_articles, name='category_articles'),
    path('activate/<uid>/<token>/', views.activate, name='activate'),

]