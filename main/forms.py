from django import forms
from .models import CoachProfile, CoachPost, CoachPhoto
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin


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


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CustomUserChangeForm(UserChangeForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]

    def clean_email(self):
        if self.cleaned_data["email"].strip() == '':
            raise ValidationError("Email is required.")
        return self.cleaned_data["email"]


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
