# Random key generation from http://djangosnippets.org/snippets/814/

from django.db import models
from django.contrib.auth.models import User
import random, string

ID_FIELD_LENGTH = 16

class Member(User):

	key = models.CharField(primary_key=True, max_length=ID_FIELD_LENGTH)
	name = models.CharField(max_length=250)
	title = models.CharField(null=True, default="", max_length=50)
	website = models.CharField(max_length=250)

	def save(self):
		if not self.key:
			self.key = random_id(ID_FIELD_LENGTH)
		super(Member, self).save()

	def __unicode__(self):
		return self.name

alphabet = string.lowercase + string.digits 
for loser in 'l1o0': # Choose to remove ones that might be visually confusing
    i = alphabet.index(loser)
    alphabet = alphabet[:i] + alphabet[i+1:]

def byte_to_base32_chr(byte):
	return alphabet[byte & 31]

def random_id(length):
	random_bytes = [random.randint(0, 0xFF) for i in range(length)]
	return ''.join(map(byte_to_base32_chr, random_bytes))