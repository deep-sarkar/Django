from django.db import models

class Room(models.Model):
	room_name  = models.CharField(max_length=20, blank=False, null=False)
	owner    = models.EmailField()

	def __str__(self):
		return self.owner

class RoomMember(models.Model):
	room_name  = models.CharField(max_length=20, blank=False, null=False)
	member = models.EmailField(null=False, blank=False)
	isAuthorized = models.BooleanField()

	def __str__(self):
		return self.member
