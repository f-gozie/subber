import string
import random


def generate_random_id(length):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def generate_public_id(parent, key, length=8):
	value = generate_random_id(length)

	if parent.objects.filter(**{key: value}).exists():
		return generate_public_id(parent, key)

	return value