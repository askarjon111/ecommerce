from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'author', 'price']
        extra_kwargs = {'author': {'read_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderItem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
