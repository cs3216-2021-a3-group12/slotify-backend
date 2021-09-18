from django.db import models
from authentication.models import User


class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.content