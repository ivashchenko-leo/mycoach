from django.contrib import admin
from .models import CoachProfile, CoachPost, Sport, CoachPhoto

# Register your models here.
admin.site.register(CoachPost)
admin.site.register(CoachProfile)
admin.site.register(CoachPhoto)
admin.site.register(Sport)