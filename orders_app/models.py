from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('in_progress', 'in_progress'), 
    ('completed', 'completed'), 
    ('cancelled', 'cancelled'), 
]

class Orders(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_customer')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_business')
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title