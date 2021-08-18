from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

	first_name = serializers.CharField()
	last_name = serializers.CharField()
	username = serializers.CharField(
		required=False,
		validators=[UniqueValidator(queryset=User.objects.all(), message='User with this username already exists')]
	)
	email = serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all(), message='User with this email already exists')]
	)
	password = serializers.CharField(min_length=8, write_only=True)


	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User.objects.create(**validated_data)
		user.set_password(password)
		user.save()
		return user


	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password', 'phone_number', 'phone_verified', 'email_verified', 'created_at', 'updated_at']