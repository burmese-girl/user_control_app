from django.contrib.auth.models import User
# from rest_framework import serializers
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate

class LoginSerializer(serializers.ModelSerializer):

	username = serializers.CharField()
	password = serializers.CharField()

	class Meta:
		model = User
		fields = ( 'username',  'password')

	def validate(self,data):
		username = data.get("username", "")
		password = data.get("password", "")	
		if username and password:
			user = authenticate(username = username, password = password)
			if user:
				if user.is_active:

					data["user"] = user
					print ("User Data" , data["user"])
				else:
					msg = "User is not active."
					raise exceptions.ValidationError(msg)
			else:
				msg= "Unable to login with given credentials."
				raise exceptions.ValidationError(msg)
		else:
			msg = "You must provide both username and password in this login API"
			raise exceptions.ValidationError(msg)

		return data 