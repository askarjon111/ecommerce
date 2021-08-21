from django.urls import path
from .views import *

urlpatterns = [
    path('', ListProducts.as_view(), name='index'),
    path('addproduct/', AddProduct.as_view(), name='addproduct'),
    path('product/<int:pk>', DetailProduct.as_view(), name="productdetail"),

    path('mycart/', MyCart.as_view(), name="mycart"),
    path('addtocart/', AddToCart.as_view(), name='addtocart'),
    path('cart/<int:pk>', CartItem.as_view(), name="cartitem"),

    path('categories/', ListCategories.as_view(), name="category"),
    path('category/<int:pk>', DetailCategory.as_view(), name="detailcategory"),

    path('orders/', ListOrders.as_view(), name="orders"),
    path('checkout/', Checkout.as_view(), name="checkout"),

    path('addreview/', AddReview.as_view(), name="addreview"),

    path('listusers/', ListUsers.as_view(), name="listusers"),
    path('registration/', UserAuth.as_view(), name='regestration'),
    path('login/', UserLogin.as_view(), name='userlogin'),
    path('profile/<int:pk>', MyProfile.as_view(), name="myprofile"),
]
