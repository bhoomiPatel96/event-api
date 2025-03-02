from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event

# Get custom user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "role"]
        # Hide Password
        extra_kwargs = {"password":{"write_only": True}}
    
    def create(self, validated_data):
        # create_user ensures the password is hashed before storing
        return User.objects.create_user(**validated_data)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "total_tickets", "tickets_sold"]