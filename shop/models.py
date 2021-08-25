from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import random


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, phone_number, password, **other_fields)

    def create_user(self, email, user_name, first_name, phone_number, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, phone_number=phone_number, ** other_fields)
        user.set_password(password)
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook',
                  'google': 'google', 'email': 'email', }

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    code = models.CharField(blank=True, null=True, max_length=15)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'phone_number']

    def __str__(self):
        return self.user_name
    
    


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images/%Y/%m/%d", blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        full_path = [self.title]
        p = self.parent
        while p is not None:
            full_path.append(p.title)
            p = p.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="product_images/%Y/%m/%d", blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=True, blank=True, default=0)
    category = models.ManyToManyField(Category)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    orderItem = models.ManyToManyField(OrderItem)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)
