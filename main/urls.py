from django.urls import path

from . import views

urlpatterns = [
    path('profiles/', views.get_profiles, name='profiles'),
    path('posts/', views.get_posts, name='posts'),
    path('posts/<uuid:post_code>', views.get_post, name='post'),
    path('profiles/<uuid:profile_code>', views.get_profile, name='profile')
]
