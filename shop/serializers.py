from rest_framework import serializers
from .models import *
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.getenv('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'author', 'price']
        extra_kwargs = {'author': {'read_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_name', 'password', 'email', 'phone_number', 'code']
        extra_kwargs = {'code': {'read_only': True}}


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'password']


class ValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['code', 'is_active']
        extra_kwargs = {'is_active': {'read_only': True}}

        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
