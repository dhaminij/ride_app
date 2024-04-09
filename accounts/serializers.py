# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

from rest_framework import serializers
from .models import Ride
from django.contrib.auth import get_user_model

User = get_user_model()


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


# class RideDetailSerializer(serializers.ModelSerializer):
#     rider = serializers.StringRelatedField()
#     driver = serializers.StringRelatedField()

#     class Meta:
#         model = Ride
#         fields = '__all__'

class RideDetailSerializer(serializers.ModelSerializer):
    rider = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()
    current_location = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = '__all__'

    def get_current_location(self, obj):
        if obj.current_location:
            return {
                'latitude': obj.current_location.y,
                'longitude': obj.current_location.x
            }
        else:
            return None

