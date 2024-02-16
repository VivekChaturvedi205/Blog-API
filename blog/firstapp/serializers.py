from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    profile_pic = serializers.ImageField(required=False)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Already registered")
        return data

    def create(self, validated_data):
        profile_pic = validated_data.pop('profile_pic', None)
        user = User.objects.create_user(username=validated_data['username'].lower(), password=validated_data['password'])
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()

        return validated_data

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        return data

    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {'message': 'Invalid username or password', 'data': {}}

        refresh = RefreshToken.for_user(user)

        return {
            'message': 'Login successful',
            'data': {'token': {'refresh_token': str(refresh), 'access_token': str(refresh.access_token)}}
        }

        