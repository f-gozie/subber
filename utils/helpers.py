import string
import random
from django.conf import settings
import redis


def generate_random_id(length):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def generate_public_id(parent, key, length=8):
	value = generate_random_id(length)

	if parent.objects.filter(**{key: value}).exists():
		return generate_public_id(parent, key)

	return value


def generate_otp(length=4):
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(length))


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)