from django.db import models
from django.contrib.auth.models import User


class OfferModel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offer_image/', blank=True, null=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.title
class DetailModel(models.Model):
    offer = models.ForeignKey(OfferModel, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
