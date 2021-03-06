import os
import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from .models import *
from .serializers import *
from .serializers import GoogleSocialAuthSerializer

load_dotenv()

client = Client(os.getenv('account'), os.getenv('token'))


# User Auth

class ListUsers(APIView):
    def get(self, request):
        permission_classes = [IsAdminUser]
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserAuth(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        account_id = os.getenv('account')
        auth_token = os.getenv('token')
        phone = request.data['phone_number']
        otp = random.randrange(100000, 999999)
        body = "Your OTP is " + str(otp)
        message = client.messages.create(to=phone, from_="+17573780739",
                                         body=body)
        if serializer.is_valid():
            serializer.validated_data['code'] = str(otp)
            user = UserProfile.objects.create_user(email=serializer.validated_data['email'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Validate(APIView):
    @swagger_auto_schema(request_body=ValidationSerializer)
    def put(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        user = UserProfile.objects.get(pk=pk)
        serializer = ValidationSerializer(user, data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']
            if code == user.code:
                user.is_verified = True
                user.code = "null"
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfile(APIView):
    def get_object(self, request):
        try:
            return UserProfile.objects.get(pk=request.user.pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = UserProfile.objects.get(pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, pk, format=None):
        user = UserProfile.objects.get(pk=request.user.pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = UserProfile.objects.get(pk=request.user.pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=ValidationSerializer)
    def put(self, request, format=None):
        permission_classes = [IsAuthenticated]
        user = request.user
        serializer = ValidationSerializer(user, data=request.data)
        if serializer.is_valid():
            code = request.data['code']
            if code == self.post.otp:
                is_active = serializer.validated_data['is_active']
                is_active = True
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
        
# Product CRUD

class ListProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AddProduct(APIView):
    # authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailProduct(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class EditProduct(APIView):
    # authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk, format=None):
        permission_classes = [IsAdminUser]
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        permission_classes = [IsAdminUser]
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Category CRUD


class ListCategories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request, format=None):
        permission_classes = [IsAdminUser]
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCategory(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        products = Product.objects.filter(category=pk).order_by('-id')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk, format=None):
        permission_classes = [IsAdminUser]
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        permission_classes = [IsAdminUser]
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Cart CRUD

class MyCart(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        permission_classes = [IsAuthenticated]
        orderitems = OrderItem.objects.filter(user=request.user)
        serializer = OrderItemSerializer(orderitems, many=True)
        return Response(serializer.data)

class AddToCart(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=OrderItemSerializer)
    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItem(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        orderitem = self.get_object(pk)
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data)

class EditCartItem(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=OrderItemEditSerializer)
    def put(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        orderitem = self.get_object(pk)
        serializer = OrderItemSerializer(orderitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCartItem(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        orderitem = self.get_object(pk)
        orderitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Order CRUD

class ListOrders(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class Checkout(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            for i in serializer.validated_data['orderItem']:
                if i.user == request.user:
                    pass
                else:
                    raise ValidationError('Bu orderitem sizniki emas')
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailOrder(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class EditOrder(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=EditOrderSerializer)
    def patch(self, request, pk, format=None):
        order = self.get_object(pk)
        orderItem = order.orderItem
        print(order.orderItem)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrder(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Review

class AddReview(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ReviewSerializer)
    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if request.data['rating'] == 0:
                raise ValidationError('Iltimos reytingni kiriting!')
                return Response(request.data['rating'], status=status.HTTP_400_BAD_REQUEST)
        elif request.data['product'] == 0:
            raise ValidationError('Iltimos mahsulotni tanlang kiriting!')
            return Response(request.data['product'], status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
