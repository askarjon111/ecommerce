import json
from rest_framework.test import APIClient, force_authenticate
from django.test import TestCase
from django import test
from django.utils import timezone
from django.urls import reverse
from .views import *
from django.contrib.auth import get_user_model


client = test.Client()

# Product Tests
class GetProductsTest(TestCase):
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


class AddValidProductTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            title="test category", slug="testcategory")

        self.valid_product = {
            'title': 'Product 1',
            'price': 500,
            'category': 1
        }

    def test_create_valid_product(self):
        client = APIClient()
        user = UserProfile.objects.create_superuser(
            email="testuser2@gmail.com",
            password="testpass"
        )
        client.force_authenticate(user=user)
        response = client.post(
            reverse('addproduct'),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddInvalidProductTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            title="test category", slug="testcategory")

        self.invalid_product = {
            'title': '',
            'price': 500,
            'category': 1
        }

    def test_create_invalid_product(self):
        client = APIClient()
        user = UserProfile.objects.create_superuser(
            email="testuser3@gmail.com",
            password="testpass"
        )
        client.force_authenticate(user=user)
        response = client.post(
            reverse('addproduct'),
            data=json.dumps(self.invalid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class EditProductTest(TestCase):
#     def setUp(self):
#         user = UserProfile.objects.create_superuser(email="test@user.com")
#         category = Category.objects.create(title="test category", slug="testcategory")

#         self.product1 = Product.objects.create(
#             title='Product 1', price=3, category=category, author=user)

#         self.valid_product = {
#             'title': 'Product 1',
#             'price': 500,
#             'category': 1
#         }

#     def test_valid_edit_product(self):
#         client = APIClient()
#         user = UserProfile.objects.create_superuser(
#             email="testuser2@gmail.com",
#             password="testpass"
#         )
#         client.force_authenticate(user=user)

#         response = client.put(
#             reverse('editproduct', kwargs={'pk': self.product1.pk}),
#             data=json.dumps(self.valid_product),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

# class TestEditInvalidProduct(TestCase):
#     def setUp(self):
#         user = UserProfile.objects.create_superuser(email="test@user.com")
#         category = Category.objects.create(
#             title="test category", slug="testcategory")

#         self.invalid_product = {
#             'title': '',
#             'price': 500,
#             'category': 1
#         }

#         self.product1 = Product.objects.create(
#             title='Product 1', price=3, category=category, author=user)

#     def test_invalid_edit_product(self):
#         client = APIClient()
#         user = UserProfile.objects.create_superuser(
#             email="testuser3@gmail.com",
#             password="testpass"
#         )
#         client.force_authenticate(user=user)

#         response = client.put(
#             reverse('editproduct', kwargs={'pk': self.product1.pk}),
#             data=json.dumps(self.invalid_product),
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCategoriesTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(
            title='Category 1', slug="category1")
        self.category2 = Category.objects.create(
            title='Category 2', slug="category2")
        self.category3 = Category.objects.create(
            title='Category 3', slug="category3")
        self.category4 = Category.objects.create(
            title='Category 4', slug="category4")

    def test_get_all_categories(self):
        # get API response
        response = client.get(reverse('category'))
        # get data from db
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_category(self):
        response = client.get(
            reverse('detailcategory', kwargs={'pk': self.category1.pk}))
        category = Category.objects.get(pk=self.category1.pk)
        serializer = CategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

