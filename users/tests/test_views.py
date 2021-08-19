from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User


class LoginViewTest(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.auth_data = {
			"email": "testcase@gmail.com",
			"password": "testcase123"
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
		'''
		response = self.client.post(self.url, self.auth_data)
		token_format = r'^\w+$'
		self.assertRegex(response.data['data']['token'], token_format)


# class CreateUsernameViewTest(TestCase):

# 	@classmethod
# 	def setUpTestData(cls):
# 		cls.auth_data = {
# 			"email": "testcase@gmail.com",
# 			"password": "testcase123"
# 		}
# 		cls.url = reverse('users:create_username')