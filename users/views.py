from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_201_CREATED
)

from .models import User
from .serializers import UserSerializer
from utils import APISuccess, APIFailure


class SignUpView(APIView):
	permission_classes = (AllowAny,)


	def post(self, request):
		serializer = UserSerializer(data=request.data, context={'request':request})
		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user=user)
				response = serializer.data
				response['token'] = token.key

				# perform any other required business logic

				return APISuccess('User created successfully', response, HTTP_201_CREATED)

		return APIFailure(serializer.errors, HTTP_400_BAD_REQUEST)


class LoginView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')
		if email is None or password is None:
			return APIFailure(
				'Please provide both email and password',
				HTTP_400_BAD_REQUEST
			)
		user = authenticate(email=email, password=password)
		if not user:
			return APIFailure(
				"Invalid login credentials",
				HTTP_404_NOT_FOUND
			)
		token, _ = Token.objects.get_or_create(user=user)
		response = UserSerializer(user).data
		response['token'] = token.key
		return APISuccess(
			'Login Successful',
			response
		)


class CreateUsernameView(APIView):

	def post(self, request):
		try:
			username = request.data.get('username')
			user = User.objects.get(id=request.user.id)
			if user.username:
				return APIFailure(
					"You already have a username",
					HTTP_400_BAD_REQUEST
				)
			if user.username == username:
				return APIFailure(
					"You cannot change your username to your current username",
					HTTP_400_BAD_REQUEST
				)

			user.username = username
			user.save()
			response = UserSerializer(user).data
			return APISuccess(
				'Username set successfully',
				response
			)
		except IntegrityError as e:
			return APIFailure(
				"There is already a user with this username",
				HTTP_400_BAD_REQUEST
			)