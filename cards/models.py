from django.db import models
from django.conf import settings

from utils.helpers import generate_public_id


class Card(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='cards'
	)
	public_id = models.CharField(max_length=10, unique=True, editable=False)
	name_on_card = models.CharField(max_length=100)
	card_pan = models.CharField(max_length=16, unique=True)
	card_hash = models.CharField(max_length=200, unique=True)
	cvv = models.CharField(max_length=3)
	expiration_date = models.DateTimeField()
	card_type = models.CharField(max_length=20)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField()

	def __str__(self):
		return f"{self.user}'s virtual card"

	def save(self, *args, **kwargs):
		if not self.pk:
			self.public_id = generate_public_id(Card, 'public_id')
		super(Card, self).save(*args, **kwargs)