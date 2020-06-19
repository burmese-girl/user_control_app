from django.shortcuts import render
from rest_framework import generics, status, exceptions
from . import serializers
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from django.db import transaction
from . import models
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ""
    serializer_class = serializers.LogoutSerializer
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        django_logout(request)
        return Response({"Logout Success."},status=200)


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UpdateUserProfileSerializer
    authentication_classes = [TokenAuthentication,BasicAuthentication]

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
