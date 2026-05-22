from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import ProfileModel

class ProfileSerializer(serializers.ModelSerializer):
    

    user = serializers.IntegerField (source='user.id', read_only=True)
    username = serializers.CharField (source='user.username', read_only=True)
    first_name = serializers.CharField (source='user.first_name')
    last_name = serializers.CharField (source='user.last_name')
    email = serializers.CharField (source='user.email')
    created_at = serializers.CharField (source='user.date_joined', read_only=True)
    type = serializers.CharField(source='user.profile.type', read_only=True)

    class Meta:
        model = ProfileModel
        fields= ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)
