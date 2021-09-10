import json
from rest_framework.test import APIClient
from django.test import TestCase
from django import test
from django.utils import timezone
from django.urls import reverse
from shop.views import *


client = test.Client()


class CartSetUp(TestCase):
    def setUp(self):
        self.author = UserProfile.objects.create_superuser(
            email="testsuper@user.com")
        self.user = UserProfile.objects.create_user(email="test@user.com")
        self.category = Category.objects.create(
            title="test category", slug="testcategory")
        self.product = Product.objects.create(
            title='Product 1', price=3, category=self.category, author=self.author)
        self.cartitem = CartItem.objects.create(
            product=self.product, qty=1, user=self.user)

        self.valid_data = {
            'product': self.product,
            'qty': 5,
            'user': self.user
        }


class AddToCartTest(CartSetUp):
    def add_to_cart(self):
        client = APIClient()
        client.force_authenticate(user=self.author)
        response = client.post(
            reverse('addtocart'),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
