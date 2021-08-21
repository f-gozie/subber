from django.test import TestCase

from users.models import User
from accounts.models import Account


class UserTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(
			first_name="Test",
			last_name="Case",
			email="testcase@gmail.com",
			password="testcase123",
			phone_number="0800000010"
		)

	def test_successful_user_creation(self):
		''' Test Case: Ensure all provided fields were created successfully
			Expected Result: Corresponding fields
		'''
		self.assertEqual(self.user.first_name, 'Test')
		self.assertEqual(self.user.last_name, 'Case')
		self.assertEqual(self.user.email, 'testcase@gmail.com')
		self.assertEqual(self.user.phone_number, '0800000010')

	def test_proper_boolean_fields(self):
		'''
			Test Case: Ensure all boolean fields were properly set to their defaults
			Expected Result: Corresponding fields
		'''
		self.assertIs(self.user.is_active, True) # Change this to false till email verification
		self.assertIs(self.user.is_staff, False)
		self.assertIs(self.user.is_superuser, False)
		self.assertIs(self.user.email_verified, False)
		self.assertIs(self.user.phone_verified, False)