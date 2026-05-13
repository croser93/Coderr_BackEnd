from rest_framework import serializers
from django.contrib.auth.models import User
from offers_app.models import OfferModel, DetailModel

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailModel
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferPostSerializer(serializers.ModelSerializer):
        
    details = DetailSerializer(many=True)
    class Meta:
        model = OfferModel
        fields = ['title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('mindestens 3 eingeben.')
        return value
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = OfferModel.objects.create(**validated_data)
        for detail in details_data:
            DetailModel.objects.create(offer=offer, **detail)
        return offer