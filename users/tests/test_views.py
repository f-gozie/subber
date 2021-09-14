from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User
from accounts.models import Account

from utils.helpers import generate_otp, redis_instance


class LoginViewTest(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.auth_data = {
			"email": "testcase@gmail.com",
			"password": "testcase123",
			"phone_number": "0800000010"
		}
		cls.url = reverse('users:login')


	def test_invalid_user(self):
		'''
			Test Case: Login with invalid credentials
			Expected Result: 404 status code with proper error message
		'''
		data = {
			"email": "bestcase@gmail.com",
			"password": "testcase122"
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['message'], "Invalid login credentials")

	def test_incomplete_credentials(self):
		'''
			Test Case: Login with incomplete credentials
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"email": "testcase@gmail.com"
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], "Please provide both email and password")

	def test_valid_user(self):
		'''
			Test Case: Login with valid credentials
			Expected Result: 200 status code with proper success message
		'''
		User.objects.create_user(**self.auth_data)

		data = {
			"email": "testcase@gmail.com",
			"password": "testcase123"
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['message'], "Login Successful")


class SignUpViewTest(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.auth_data = {
			"first_name": "Test",
			"last_name": "Case",
			"email": "testcase@gmail.com",
			"password": "testcase123",
			"phone_number": "08000000010"
		}
		cls.url = reverse('users:signup')

	def test_create_user(self):
		'''
			Test Case: Create user with required credentials
			Expected Result: 201 status code with proper success message
		'''
		response = self.client.post(self.url, self.auth_data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['message'], 'User created successfully')

	def test_incomplete_create_user(self):
		'''
			Test Case: Create user with incomplete credentials
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"email": "testcase@gmail.com"
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, 400)

	def test_token_creation(self):
		'''
			Test Case: Ensure that token was created upon user creation
			Expected Result: Token with the expected 'token_format'
		'''
		response = self.client.post(self.url, self.auth_data)
		token_format = r'^\w+$'
		self.assertRegex(response.data['data']['token'], token_format)

	def test_accounts_creation(self):
		'''
			Test Case: Ensure that user accounts (ngn and usd) are created alongside user creation
			Expected Result: 2 accounts associated with the user
		'''
		user = User.objects.create_user(**self.auth_data)
		accounts = Account.objects.filter(user=user)
		self.assertEqual(len(accounts), 2)
		self.assertEqual(set([account.get_currency_display() for account in accounts]), set(['ngn', 'usd']))


class CreateUsernameViewTest(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_data = {
			"email": "testcase@gmail.com",
			"password": "testcase123",
			"phone_number": "0800000010"
		}
		cls.user = User.objects.create_user(**cls.user_data)
		cls.url = reverse('users:create_username')

	# def test_email_otp_sent(self):
	# 	'''
	# 		Test Case: Check if email is sent successfully
	# 	'''
	# 	proper_url =


	def test_username_creation(self):
		'''
			Test Case: Create username for existing user
			Expected Result: 200 status code with proper success message
		'''
		data = {
			"username": "danny"
		}
		self.client.force_authenticate(self.user)
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['message'], "Username set successfully")

	def test_already_has_username(self):
		'''
			Test Case: Create username for user that already has username
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"username": "danny"
		}
		self.client.force_authenticate(self.user)

		self.user.username = "danny"
		self.user.save()
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], "You already have a username")

	def test_username_already_exists(self):
		'''
			Test Case: Create username for user with a username that exists
			Expected Result: 400 status code with proper error message
		'''
		new_user_data = {
			"email": "testcase2@gmail.com",
			"password": "testcase122",
			"username": "barney",
			"phone_number": "0800000020"
		}
		User.objects.create_user(**new_user_data)

		data = {
			"username": "barney"
		}
		self.client.force_authenticate(self.user)
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], "There is already a user with this username")

class VerifyEmailViewTest(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_data = {
			"email": "testcase@gmail.com",
			"password": "testcase123",
			"phone_number": "08000000010"
		}
		cls.user = User.objects.create_user(**cls.user_data)
		cls.otp = generate_otp(4)
		redis_instance.hmset(cls.user.email, {'otp': cls.otp})
		redis_instance.expire(cls.user.email, 300)
		cls.url = reverse('users:verify_email')

	def test_email_already_verified(self):
		'''
			Test Case: Try to verify the email of an already an already email-verified user
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"otp": 'ABCD'
		}
		self.client.force_authenticate(self.user)
		self.user.email_verified = True
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], 'Your email is already verified')

	def test_email_verified_successful(self):
		'''
			Test Case: Verify email address with provided otp code
			Expected Result: 200 status code with proper success message
		'''
		redis_otp = redis_instance.hmget(self.user.email, 'otp')
		proper_otp = str(redis_otp[0].decode('utf-8'))
		data = {
			"otp": proper_otp
		}
		self.client.force_authenticate(self.user)
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['message'], 'Email address verified successfully')

	def test_invalid_otp_code(self):
		'''
			Test Case: Fail requests with invalid OTP code
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"otp": "ABCD"
		}
		self.client.force_authenticate(self.user)
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], 'Invalid OTP code')

	def test_xpired_otp_code(self):
		'''
			Test Case: Fail requests if OTP code has expired
			Expected Result: 400 status code with proper error message
		'''
		data = {
			"otp": "ABCD"
		}
		redis_instance.delete(self.user.email)
		self.client.force_authenticate(self.user)
		response = self.client.post(self.url, data)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['message'], 'OTP code expired or invalid')