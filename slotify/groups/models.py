from django.db import models
from authentication.models import User

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    banner_url = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    tag = models.ForeignKey('Tag', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user} {self.group}")
