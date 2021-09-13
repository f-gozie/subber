from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_201_CREATED
)

from .models import User
from .serializers import UserSerializer
from services.notification.sendgrid import send_email
from utils import APISuccess, APIFailure
from utils.helpers import generate_otp


class SignUpView(APIView):
	permission_classes = (AllowAny,)


	def post(self, request):
		serializer = UserSerializer(data=request.data, context={'request':request})
		if serializer.is_valid():
			email = serializer.validated_data.get('email')
			otp_code = generate_otp(4)
			send_email(to=email, otp_code=otp_code)
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

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return APISuccess(
            'Token retrieved successfully',
            {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            },
            HTTP_200_OK
        )

class CreateUsernameView(APIView):
	# check if user is authenticated and return an error if they are not
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		try:
			username = request.data.get('username')
			user = User.objects.get(id=request.user.id)
			if user.username:
				return APIFailure(
					"You already have a username",
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