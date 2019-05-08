from django.urls import path

from . import views

urlpatterns = [
    path('sports/', views.get_sports, name='sports'),
    path('profiles/', views.get_profiles, name='profiles'),
    path('posts/', views.get_posts, name='posts'),
    path('posts/<uuid:post_code>', views.get_post, name='post'),
    path('profiles/<uuid:profile_code>', views.get_profile, name='profile'),
    path('signin', views.sign_in, name='sign_in'),
    path('posts/my', views.get_my_posts, name='my_posts'),
    path('posts/my/<uuid:post_code>', views.get_my_post, name='my_post'),
    path('posts/add', views.add_post, name='add_post'),
    path('posts/update/<uuid:post_code>', views.update_post, name='update_post'),
    path('posts/remove/<uuid:post_code>', views.remove_post, name='remove_post'),
    path('photos/', views.get_photos, name='get_photos'),
    path('photos/add', views.add_photos, name='add_photos'),
    path('photos/remove/<uuid:photo_code>', views.remove_photo, name='remove_photo')
]
