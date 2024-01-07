'''This file contains the custom middlewares for the backend'''

# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from urllib.parse import urljoin
from oauth2_provider.models import AccessToken
from datetime import timedelta, timezone
import requests


class TokenRefreshMiddleware(MiddlewareMixin):
    '''This middleware refreshes the access token if it is about to expire'''
    def process_request(self, request):
        if request.user.is_authenticated:
            token = AccessToken.objects.filter(user=request.user).first()
            # If the token is about to expire in the next 2 minutes
            if token and token.expires < timezone.now() + timedelta(seconds=600):
                response = requests.post(urljoin(settings.BASE_URL, 'o/token/'), data={
                    'grant_type': 'refresh_token',
                    'refresh_token': token.refresh_token,
                    'client_id': settings.OAUTH_CLIENT_ID,
                    'client_secret': settings.OAUTH_CLIENT_SECRET,
                })
                if response.status_code == 200:
                    token.token = response.json()['access_token']
                    token.expires = timezone.now(
                    ) + timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
                    token.save()
