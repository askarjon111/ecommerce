from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    # _id = models.AutoField(primary_key=True, editable=False)

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



