from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
<<<<<<< HEAD:news/urls.py
    path('', views.index, name='index'),
    path('add/', views.add_post, name='add-post'),
    path('categories/', views.categories, name='categories'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('set-language/', views.set_language, name='set_language'),
    path('api/weather/', views.weather_api, name='api-weather'),
=======
    path('', views.index, name='news-index'),
    path('add_post/', views.add_post, name='news-add-post'),
>>>>>>> 004ab6783df51e7660ea2dd5a0182e380bcfb5d7:newsapp/urls.py
]
