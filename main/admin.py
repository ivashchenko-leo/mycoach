from django.contrib import admin
from .models import CoachProfile, CoachPost, Sport, CoachPhoto
from django.contrib.auth.models import User
from .forms import CustomUserAdmin

# Register your models here.
admin.site.register(CoachPost)
admin.site.register(CoachProfile)
admin.site.register(CoachPhoto)
admin.site.register(Sport)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)