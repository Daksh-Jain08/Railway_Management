from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            existing_user = self.get_user(email)
            if existing_user:
                sociallogin.connect(request, existing_user)
            else:
                raise PermissionDenied("Email not found.")

    def get_user(self, email):
        try:
            return get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return None