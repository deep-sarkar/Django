from django.db import models


class GroupChat(models.Model):
	owner	  = models.CharField(max_length=50)
	room_name = models.CharField(max_length=20)
	

	def __str__(self):
		return self.room_name

class GroupMembers(models.Model):
	room_name	 = models.CharField(max_length=20)
	member 	  	 = models.CharField(max_length=20)
	isAuthorised = models.BooleanField(default=False)

	def __str__(self):
		return self.room_name