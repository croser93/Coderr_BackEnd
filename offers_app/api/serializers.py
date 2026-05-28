from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Min
from offers_app.models import OfferModel, DetailModel

class UserSerializer(serializers.ModelSerializer):
    
    """
    
    Serializer for User information. 
    
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class DetailSerializer(serializers.ModelSerializer):
    
    """
    
    Serializer for Details in Offers. 
    
    """
    class Meta:
        model = DetailModel
        fields = ['id','title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferPostSerializer(serializers.ModelSerializer):
    
    """
    
    Serializer for POST Offers.
    
    details = from DetailSerializer
    validate_details = Validate min 3. 
    create = Create a Offer
    
    """
        
    details = DetailSerializer(many=True)
    class Meta:
        model = OfferModel
        fields = ['id', 'title', 'image', 'description', 'details']

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
    
    """
    
    Serializer for GET & Delete Offers.
    
    user_details = from UserSerializer
    min_price = return the smallest price in details
    min_delivery_time = return the smallest delivery_time_in_days in details
    details = from DetailSerializer
    
    """

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
    
class OfferDetailPatchSerializer(serializers.ModelSerializer):

    """
    
    Serializer for Patch Offers.
    
    details = from DetailSerializer
    
    """
    details = DetailSerializer(many=True, required=False)

    class Meta:
        model = OfferModel
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        instance = super().update(instance, validated_data)
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    DetailModel.objects.filter(offer=instance, offer_type=offer_type).update(**detail_data)
        return instance

    
class OfferDetailSerializer(OfferGetSerializer):
    
    
    """
    
    Serializer for GET offerdetails.
    
    """
    
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = OfferModel
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    
class OfferDetailsIdSerializer(DetailSerializer):
    """
    
    Serializer for GET offerdetails id.
    
    """
    
    class Meta:
        model = DetailModel
        fields = ['id','title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
