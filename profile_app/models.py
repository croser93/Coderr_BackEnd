from django.db import models
from django.contrib.auth.models import User

class Profiles(models.Model):
    class Meta:
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(User,on_delete=models.CASCADE,  related_name='profile_detail' )
    file = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.CharField( max_length=50, blank=True)
    working_hours =  models.CharField( max_length=50, blank=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

