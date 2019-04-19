from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Prefetch, prefetch_related_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBadRequest, JsonResponse
from .models import CoachProfile, CoachPost


def profiles(request: HttpRequest) -> HttpResponse:
    public_profiles = CoachProfile.objects.filter(is_public=True)\
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name')\
        .annotate(sports=ArrayAgg('sports__name'), photos=ArrayAgg('photos__image', True))\

    result = []
    for profile in public_profiles:
        profile['coach'] = profile.pop('user__first_name', '') + ' ' + profile.pop('user__last_name', '')
        result.append(profile)

    return JsonResponse(result, safe=False)


def posts(request: HttpRequest) -> HttpResponse:
    public_posts = CoachPost.objects.filter(is_public=True)\
        .values('code', 'user', 'timestamp', 'title', 'tags')

    return JsonResponse(list(public_posts), safe=False)
