from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import Profiles
from django.utils import timezone

class ProfileSerializer(serializers.ModelSerializer):
    
    """
    Serializer for add a Profile for the User.
    
    It is created during registration and populated with data.
    
    """
    

    user = serializers.IntegerField (source='user.id', read_only=True)
    username = serializers.CharField (source='user.username', read_only=True)
    first_name = serializers.CharField (source='user.first_name')
    last_name = serializers.CharField (source='user.last_name')
    email = serializers.CharField (source='user.email')
    created_at = serializers.DateTimeField (source='user.date_joined', read_only=True)
    type = serializers.CharField(source='user.profile.type', read_only=True)


    class Meta:
        model = Profiles
        fields= ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'file' in validated_data:
            instance.uploaded_at = timezone.now()
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)
    


class ProfilesBusinessSerializer(ProfileSerializer):
    class Meta:
        model = Profiles
        fields= ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]

class ProfilesCustomersSerializer(ProfileSerializer):
    uploaded_at = serializers.DateTimeField(read_only=True, allow_null=True, format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Profiles
        fields= ["user", "username", "first_name", "last_name", "file", "uploaded_at", "type"]