import uuid as _uuid

from django.contrib.auth import login
from django.views import View
from django.shortcuts import render, redirect

from apps.users.models import UserToken


class LoginView(View):
    def get(self, request, token: _uuid.UUID):
        user_token = UserToken.objects.filter(uuid=token, is_used=False).order_by("-created_at").first()
        if user_token:
            if user_token.is_active:
                user_token.is_used = True
                user_token.save()
                login(request, user_token.user)
                return redirect("index")
        return redirect("index")
