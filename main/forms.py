from django import forms
from .models import CoachProfile, CoachPost, CoachPhoto
from rest_framework import serializers


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
