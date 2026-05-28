from rest_framework import serializers
from reviews_app.models import Reviews
from auth_app.models import UserProfile
from offers_app.models import Offers
from django.db.models import Avg

class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for Base Information for Site.
    
    calculated fields:
    - review_count = return all counts of reviews.
    - average_rating  = return average rating of all reviews.
    - business_profile_count = return the count of all Business Profiles.
    - offer_count  = return the count of offers.
    """

    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        return Reviews.objects.count()
    
    def get_average_rating(self, obj):
        return Reviews.objects.aggregate(Avg('rating'))['rating__avg']

    def get_business_profile_count(self, obj):
        return UserProfile.objects.filter(type='business').count()

    def get_offer_count(self, obj):
        return Offers.objects.count()