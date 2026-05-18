from rest_framework import serializers
from reviews_app.models import ReviewModel
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReviewModel
        fields = ['id', "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ['reviewer']
    
   
    