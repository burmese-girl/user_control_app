from django.contrib.auth.models import User
# from rest_framework import serializers
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from . import models


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                    print ("User Data", data["user"])
                else:
                    msg = "User is not active."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "You must provide both username and password in this login API"
            raise exceptions.ValidationError(msg)

        return data


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('country_code', 'phone_num', 'dob', 'gender',)


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(source='profile.country_code', required=False, allow_blank=True)
    phone_num = serializers.CharField(source='profile.phone_num', required=False, allow_blank=True)
    gender = serializers.CharField(source='profile.gender', required=False, allow_blank=True)
    dob = serializers.CharField(source='profile.dob', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country_code', 'phone_num', 'dob', 'gender',)

    def update(self, instance, data):
        # import pdb;pdb.set_trace() #for debugging
        if instance:
            instance.first_name = data.get('first_name', instance.first_name)
            instance.last_name = data.get('last_name', instance.last_name)
            instance.userprofile.country_code = data.get('first_name', instance.userprofile.country_code)
            instance.userprofile.phone_num = data.get('phone_num', instance.userprofile.phone_num)
            instance.userprofile.gender = data.get('gender', instance.userprofile.gender)
            instance.userprofile.dob = data.get('dob', instance.userprofile.dob)
            instance.save()
        else:
            message = "Serializers User not found with your credentials."
            raise exceptions.ValidationError(message)

        return instance
