from rest_framework import serializers
from .models import Profile, SpendAmount
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=5)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password', 
            'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class SpendAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendAmount
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    spendamount_set = SpendAmountSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'