from uuid import UUID

from django.contrib.auth import authenticate
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_200_OK

from .authentication import token_expire_handler, expires_in, IsCoach
from .forms import CoachPhotoForm, CoachPostForm, CoachProfileForm, UserSigninSerializer
from .models import CoachProfile, CoachPost, CoachPhoto, Sport


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_sports(request: HttpRequest) -> HttpResponse:
    sports = Sport.objects.all()

    return JsonResponse([{'code': sport.code, 'name': sport.name} for sport in sports], safe=False)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_profiles(request: HttpRequest) -> HttpResponse:
    public_profiles = CoachProfile.objects.filter(is_public=True)\
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name')\
        .annotate(sports=ArrayAgg('sports__name', True), photos=ArrayAgg('photos__image', True))\

    result = []
    for profile in public_profiles:
        profile['owner'] = profile.pop('user__first_name', '') + ' ' + profile.pop('user__last_name', '')
        result.append(profile)

    return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_posts(request: HttpRequest) -> HttpResponse:
    public_posts = CoachPost.objects.filter(is_public=True)\
        .values('code', 'user__first_name', 'user__last_name', 'timestamp', 'title', 'tags', 'content')

    result = []
    for post in public_posts:
        post['author'] = post.pop('user__first_name', '') + ' ' + post.pop('user__last_name', '')
        result.append(post)

    return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_profile(request: HttpRequest, profile_code: UUID) -> HttpResponse:
    profiles = CoachProfile.objects.filter(code=profile_code, is_public=True)\
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name', 'content') \
        .annotate(sports=ArrayAgg('sports__name', True), photos=ArrayAgg('photos__image', True))

    if not profiles:
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    profiles[0]['owner'] = profiles[0].pop('user__first_name', '') + ' ' + profiles[0].pop('user__last_name', '')

    return JsonResponse(profiles[0])


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_post(request: HttpRequest, post_code: UUID) -> HttpResponse:
    post = get_object_or_404(CoachPost, pk=post_code, is_public=True)
    author = post.user.first_name + ' ' + post.user.last_name

    return JsonResponse({'author': author, 'content': post.content, 'tags': post.tags,
                         'timestamp': post.timestamp, 'title': post.title})


@api_view(["GET"])
@permission_classes((IsCoach,))
def get_my_post(request: HttpRequest, post_code: UUID) -> HttpResponse:
    post = get_object_or_404(CoachPost, pk=post_code, user=request.user)
    author = post.user.first_name + ' ' + post.user.last_name

    return JsonResponse({'author': author, 'content': post.content, 'tags': post.tags,
                         'timestamp': post.timestamp, 'is_public': post.is_public, 'title': post.title})


@api_view(["GET"])
@permission_classes((IsCoach,))
def get_my_posts(request: HttpRequest) -> HttpResponse:
    my_posts = CoachPost.objects.filter(user=request.user)\
        .values('code', 'user__first_name', 'user__last_name', 'timestamp', 'title', 'tags', 'content', 'is_public')

    result = []
    for post in my_posts:
        post['author'] = post.pop('user__first_name', '') + ' ' + post.pop('user__last_name', '')
        result.append(post)

    return JsonResponse(result, safe=False)


@api_view(["POST"])
@permission_classes((IsCoach,))
def add_post(request: HttpRequest) -> HttpResponse:
    form = CoachPostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()

        return HttpResponse(status=HTTP_200_OK)
    return JsonResponse(form.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsCoach,))
def update_post(request: HttpRequest, post_code: UUID) -> HttpResponse:
    post = get_object_or_404(CoachPost, code=post_code, user=request.user)
    form = CoachPostForm(request.POST)
    if form.is_valid():
        post.title = form.cleaned_data["title"]
        post.content = form.cleaned_data["content"]
        post.is_public = form.cleaned_data["is_public"]
        post.tags = form.cleaned_data["tags"]
        post.save()

        return HttpResponse(status=HTTP_200_OK)
    return JsonResponse(form.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsCoach,))
def remove_post(request: HttpRequest, post_code: UUID) -> HttpResponse:
    CoachPost.objects.filter(pk=post_code, user=request.user).delete()

    return HttpResponse(status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsCoach,))
def get_photos(request: HttpRequest) -> HttpResponse:
    photos = CoachPhoto.objects.filter(user=request.user)\
        .values('code', 'image')

    return JsonResponse([photo for photo in photos], safe=False)


@api_view(["POST"])
@permission_classes((IsCoach,))
def add_photos(request: HttpRequest) -> HttpResponse:
    images = request.FILES.getlist(key='image')
    if not images:
        return JsonResponse({'error': ['No images to save']}, status=HTTP_400_BAD_REQUEST)

    for image in images:
        request.FILES['image'] = image
        form = CoachPhotoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
        else:
            return JsonResponse(form.errors, status=HTTP_400_BAD_REQUEST)

    return HttpResponse(status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsCoach,))
def remove_photo(request: HttpRequest, photo_code: UUID) -> HttpResponse:
    CoachPhoto.objects.filter(pk=photo_code, user=request.user).delete()

    return HttpResponse(status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsCoach,))
def add_profile(request: HttpRequest) -> HttpResponse:
    profiles = CoachProfile.objects.filter(user=request.user)

    if profiles:
        return JsonResponse({'error': ['Profile already exists']}, status=HTTP_400_BAD_REQUEST)

    form = CoachProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()

        profile.sports.set(Sport.objects.filter(code__in=request.POST['sports'].split(",")))
        profile.photos.set(CoachPhoto.objects.filter(code__in=request.POST['photos'].split(",")))

        return HttpResponse(status=HTTP_200_OK)
    return JsonResponse(form.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsCoach,))
def update_profile(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(CoachProfile, user=request.user)

    form = CoachProfileForm(request.POST)
    if form.is_valid():
        profile.description = form.cleaned_data["description"]
        profile.timestamp = now()
        profile.content = form.cleaned_data["content"]
        profile.is_public = form.cleaned_data["is_public"]
        profile.user = request.user
        profile.save()

        profile.sports.set(Sport.objects.filter(code__in=request.POST['sports'].split(",")))
        profile.photos.set(CoachPhoto.objects.filter(code__in=request.POST['photos'].split(",")))

        return HttpResponse(status=HTTP_200_OK)
    return JsonResponse(form.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsCoach,))
def remove_profile(request: HttpRequest) -> HttpResponse:
    CoachProfile.objects.filter(user=request.user).delete()

    return HttpResponse(status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsCoach,))
def get_my_profile(request: HttpRequest) -> HttpResponse:
    profiles = CoachProfile.objects.filter(user=request.user) \
        .values('code', 'description', 'timestamp', 'user__first_name', 'user__last_name', 'content', 'is_public') \
        .annotate(sports=ArrayAgg('sports__name', True), photos=ArrayAgg('photos__image', True))

    if not profiles:
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    profiles[0]['owner'] = profiles[0].pop('user__first_name', '') + ' ' + profiles[0].pop('user__last_name', '')

    return JsonResponse(profiles[0])


@api_view(["POST"])
@permission_classes((AllowAny,))
def sign_in(request: HttpRequest) -> HttpResponse:
    sign_in_serializer = UserSigninSerializer(data=request.POST)
    if not sign_in_serializer.is_valid():
        return JsonResponse(sign_in_serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=sign_in_serializer.data['username'], password=sign_in_serializer.data['password'])
    if not user:
        return JsonResponse({'error': ['Invalid credentials']}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)
    user_serialized = {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}

    response = JsonResponse({'user': user_serialized, 'expires_in': expires_in(token), 'token': token.key})
    response.set_cookie('token', token.key, httponly=True)

    return response
