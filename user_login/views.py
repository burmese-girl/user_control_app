from django.shortcuts import render
from rest_framework import generics,status, exceptions
from . import serializers 
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework.response import Response



# Create your views here.

class LoginView(generics.CreateAPIView):

	permission_classes = []
	queryset = ""
	serializer_class =serializers.LoginSerializer #you need serializer

	def post(self,request):		
		transaction.atomic()
		serializer = serializers.LoginSerializer(data = request.data)		
		serializer.is_valid(raise_exception=True)		
		user = serializer.validated_data["user"]			
		django_login(request,user)
		token, created=Token.objects.get_or_create(user=user)
		return  Response( { "token" : token.key}, status=200)
		


# class LogoutView(APIView):
# 	pass