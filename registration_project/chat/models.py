from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='user', db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient', related_name='recipient', db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index = True)
    body      = models.TextField(max_length=500)

    def __str__(self):
        return self.user
