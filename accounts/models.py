from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from utils.helpers import generate_public_id
from utils.choices import Account as AccountChoices


class Account(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='accounts'
	)
	public_id = models.CharField(max_length=10, unique=True, editable=False)
	currency = models.PositiveSmallIntegerField(
		choices=AccountChoices.CURRENCY_CHOICES,
		default=AccountChoices.NAIRA
	)
	balance = models.DecimalField(
		default=0.00,
		decimal_places=2,
		max_digits=12,
		validators=[MinValueValidator(Decimal(0.00))]
	)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user}'s account"

	def save(self, *args, **kwargs):
		if not self.pk:
			self.public_id = generate_public_id(Account, 'public_id')
		super(Account, self).save(*args, **kwargs)