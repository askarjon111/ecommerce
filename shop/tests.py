import json
from django.test import TestCase
from django import test
from django.utils import timezone
from django.urls import reverse
from .views import *

client = test.Client()

class GetAllProductsTest(TestCase):
    """ Test module for GET all products API """
    
    def setUp(self):
        user = UserProfile.objects.create_superuser(email="test@user.com")
        category = Category.objects.create(title="test category", slug="testcategory")
        self.product1 = Product.objects.create(
            title='Product 1', price=3, category=category, author=user)
        self.product2 = Product.objects.create(
            title='Product 2', price=1, category=category, author=user)
        self.product3 = Product.objects.create(
            title='Product 3', price=2, category=category, author=user)
        self.product4 = Product.objects.create(
            title='Product 4', price=6, category=category, author=user)

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('index'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('productdetail', kwargs={'pk': self.product1.pk}))
        product = Product.objects.get(pk=self.product1.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('productdetail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddProductTest(TestCase):
    def setUp(self):
        user = UserProfile.objects.create_superuser(email="test@user.com")
        category = Category.objects.create(
            title="test category", slug="testcategory")
            
        self.valid_product = {
            'title': 'Product1',
            'price': 500,
            'category': 1,
            'author': 1,
        }
        self.invalid_product = {
            'title': '',
            'price': 500,
            'category': 1,
            'author': 1,
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('addproduct'),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('addproduct'),
            data=json.dumps(self.invalid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
