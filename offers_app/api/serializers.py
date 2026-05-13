from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Min
from offers_app.models import OfferModel, DetailModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailModel
        fields = ['id','title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

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
    
class OfferGetSerializer(serializers.ModelSerializer):

    user_details = UserSerializer(source='user', read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    class Meta:
        model = OfferModel
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details' ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']
    
    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']
    
    def get_details(self, obj):
        return [{
            'id': detail.id,
            'url': f'/offerdetails/{detail.id}/'} for detail in obj.details.all()]

    
