from rest_framework import serializers
from reviews_app.models import ReviewModel
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReviewModel
        fields = ['id', "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ['reviewer']

    def validate(self, data):
        if ReviewModel.objects.filter(reviewer=self.context['request'].user, business_user=data['business_user']).exists():
            raise serializers.ValidationError({'error': 'Du hast diesen Business-User bereits bewertet.'})
        return data
    
   
    