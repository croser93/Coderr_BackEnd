from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from auth_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):

    TYPE_CHOICES = [
        ('customer', 'customer'),
        ('business', 'business')
    ]
    type = serializers.ChoiceField(choices = TYPE_CHOICES)
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(validators=[RegexValidator(r'^[a-zA-ZäöüÄÖÜß\s]+$', 'Only letters and spaces allowed.')])
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    
    def validate_username(self, value):
        if len(value.split()) < 2:
            raise serializers.ValidationError({'error': 'Enter your Firstname and Lastname'})
        return value

    def save(self, **kwargs):
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']
        username = self.validated_data['username']
        user_type = self.validated_data['type']

        name_parts = username.split()
        first_name = name_parts[0]
        last_name  = ' '.join(name_parts[1:])

        all_emails = User.objects.values_list('email', flat=True)

        if pw != repeated_password:
            raise serializers.ValidationError({'error': 'password dont match'})

        if email in all_emails:
            raise serializers.ValidationError({'error': 'email is used'})

        account = User(
            email = email,
            username = first_name + '-' + last_name,
            first_name = first_name,
            last_name = last_name,
        )

        account.set_password(pw)
        account.save()
        UserProfile.objects.create(user=account, type=user_type)
        return account