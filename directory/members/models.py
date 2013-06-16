from django.db import models
from django.contrib.auth.models import User

class Member(User):
	name = models.CharField(max_length=250)
	title = models.CharField(null=True, default="", max_length=50)
	website = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name