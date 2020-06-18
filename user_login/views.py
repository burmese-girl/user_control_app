from django.shortcuts import render
from rest_framework import generics, status, exceptions
from . import serializers
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from . import models
from rest_framework.response import Response


# Create your views here.

class LoginView(generics.CreateAPIView):
    permission_classes = []
    queryset = ""
    serializer_class = serializers.LoginSerializer  # you need serializer

    def post(self, request):
        transaction.atomic()
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = ""
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    queryset = ""
    serializer_class = serializers.UpdateUserProfileSerializer

    # current user
    def get_object(self):
        return self.request.user

    def update(self, request):
        user_instance = self.get_object()
        user_ser = serializers.UpdateUserProfileSerializer(user_instance, data=request.data)
        user_ser.is_valid(raise_exception=True)
        user_ser.save()

        profile = models.UserProfile.objects.get(user_id=user_instance.pk)
        update_data = request.data
        profile_ser = serializers.ProfileSerializer(profile, data=update_data)
        profile_ser.is_valid(raise_exception=True)
        profile_ser.save()

        return Response(user_ser.validated_data, status=200)
