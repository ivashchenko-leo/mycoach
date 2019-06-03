from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework import exceptions

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from django.utils.translation import gettext
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    """
    If token is expired new token will be established
    If token is expired then it will be removed and new one with different key will be created
    """

    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate(self, request: HttpRequest):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            if 'token' not in request.COOKIES.keys():
                return None

            token = request.COOKIES['token']
        else:
            if len(auth) == 1:
                msg = gettext('Invalid token header. No credentials provided.')
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = gettext('Invalid token header. Token string should not contain spaces.')
                raise exceptions.AuthenticationFailed(msg)

            try:
                token = auth[1].decode()
            except UnicodeError:
                msg = gettext('Invalid token header. Token string should not contain invalid characters.')
                raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """
            If token is expired then it will be removed and new one with different key will be created
        """

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed(gettext("Invalid Token"))

        if not token.user.is_active:
            raise AuthenticationFailed(gettext("User is not active"))

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed(gettext("The Token is expired"))

        return token.user, token


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None


class IsCoach(BasePermission):
    """
    Allows to have access only to coaches or staff.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Coaches').exists() or request.user.is_staff
