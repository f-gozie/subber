from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
	username = models.CharField(max_length=100, unique=True, blank=True, null=True)
	email = models.EmailField(_('email address'), unique=True)
	phone_number = models.CharField(max_length=20, unique=True)
	phone_verified = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	# uncomment after creating corresponding apps and models
	'''
	def get_naira_balance(self):
		return self.cards_set.get(currency=Cards.NAIRA).balance

	def get_dollar_balance(self):
		return self.cards_set.get(currency=Cards.DOLLAR).balance
	'''
