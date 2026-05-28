from django.db import models
from django.contrib.auth.models import User


class Offers(models.Model):

    class Meta:
        verbose_name_plural = 'Offers'

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offer_image/', blank=True, null=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
class OffersDetail(models.Model):

    class Meta:
        verbose_name_plural = 'OffersDetails'
        
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
