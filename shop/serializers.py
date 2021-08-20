from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import UserProfile


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
        fields = ['user_name', 'password', 'email']
        

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
