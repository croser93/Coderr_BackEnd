from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    TYPE_CHOICES = [
        ('customer', 'customer'),
        ('business', 'business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
