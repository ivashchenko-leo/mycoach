from django.urls import path

from . import views

urlpatterns = [
    path('profiles/', views.profiles, name='profiles'),
    path('posts/', views.posts, name='posts')
]