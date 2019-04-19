from django.contrib.postgres.aggregates import ArrayAgg
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBadRequest, JsonResponse
from .models import CoachProfile, CoachPost


def get_profiles(request: HttpRequest) -> HttpResponse:
    public_profiles = CoachProfile.objects.filter(is_public=True)\
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name')\
        .annotate(sports=ArrayAgg('sports__name'), photos=ArrayAgg('photos__image', True))\

    result = []
    for profile in public_profiles:
        profile['owner'] = profile.pop('user__first_name', '') + ' ' + profile.pop('user__last_name', '')
        result.append(profile)

    return JsonResponse(result, safe=False)


def get_posts(request: HttpRequest) -> HttpResponse:
    public_posts = CoachPost.objects.filter(is_public=True)\
        .values('code', 'user__first_name', 'user__last_name', 'timestamp', 'title', 'tags', 'content')

    result = []
    for post in public_posts:
        post['author'] = post.pop('user__first_name', '') + ' ' + post.pop('user__last_name', '')
        result.append(post)

    return JsonResponse(result, safe=False)


def get_profile(request: HttpRequest, profile_code: UUID) -> HttpResponse:
    profiles = CoachProfile.objects.filter(code=profile_code, is_public=True)\
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name', 'content') \
        .annotate(sports=ArrayAgg('sports__name'), photos=ArrayAgg('photos__image', True))

    if not profiles:
        raise Http404()

    profiles[0]['owner'] = profiles[0].pop('user__first_name', '') + ' ' + profiles[0].pop('user__last_name', '')

    return JsonResponse(profiles[0])


def get_post(request: HttpRequest, post_code: UUID) -> HttpResponse:
    post = get_object_or_404(CoachPost, pk=post_code, is_public=True)
    author = post.user.first_name + ' ' + post.user.last_name

    return JsonResponse({'author': author, 'content': post.content, 'tags': post.tags,
                         'timestamp': post.timestamp, 'title': post.title})
