from django import forms
from .models import CoachProfile, CoachPost, CoachPhoto


class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = CoachProfile
        fields = ('description', 'content', 'is_public', 'sports', 'photos')


class CoachPhotoForm(forms.ModelForm):
    class Meta:
        model = CoachPhoto
        fields = ('image',)


class CoachPostForm(forms.ModelForm):
    class Meta:
        model = CoachPost
        fields = ('title', 'content', 'is_public', 'tags')
