from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


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
        fields = ['user_name', 'password', 'email', 'phone']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if UserProfile.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'password']
        

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
