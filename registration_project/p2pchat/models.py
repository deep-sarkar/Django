from django.db import models

class Message(models.Model):
    stream    = models.CharField(max_length=50, blank=False, null=False) 
    sender    = models.CharField(max_length=20, blank=False, null=False)
    receiver  = models.CharField(max_length=20, blank=False, null=False)
    body      = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stream

class Meta:
    ordering = ['-timestamp']

