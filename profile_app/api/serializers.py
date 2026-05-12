from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import ProfileModel

class ProfileListSerializer(serializers.ModelSerializer):
    

    user = serializers.IntegerField (source='user.id', read_only=True)
    username = serializers.CharField (source='user.username', read_only=True)
    first_name = serializers.CharField (source='user.first_name', read_only=True)
    last_name = serializers.CharField (source='user.last_name', read_only=True)
    email = serializers.CharField (source='user.email', read_only=True)
    created_at = serializers.CharField (source='user.date_joined', read_only=True)
    type = serializers.CharField(source='user.profile.type', read_only=True)

    class Meta:
        model = ProfileModel
        fields= ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]
