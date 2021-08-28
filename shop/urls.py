from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Product CRUD
    path('products/', ListProducts.as_view(), name='index'),
    path('products/addproduct/', AddProduct.as_view(), name='addproduct'),
    path('products/<int:pk>',
         DetailProduct.as_view(), name="productdetail"),
    path('products/edit/<int:pk>', EditProduct.as_view(), name="editproduct"),
    path('products/delete/<int:pk>', DeleteProduct.as_view(), name="deleteproduct"),
    
    # Cart  CRUD
    path('mycart/', MyCart.as_view(), name="mycart"),
    path('mycart/add/', AddToCart.as_view(), name='addtocart'),
    path('mycart/<int:pk>', CartItem.as_view(), name="cartitemdetail"),
    path('mycart/edit/<int:pk>', EditCartItem.as_view(), name="editcartitem"),
    path('mycart/delete/<int:pk>', DeleteCartItem.as_view(), name="deletecartitem"),

    # Category CRUD
    path('categories/', ListCategories.as_view(), name="category"),
    path('categories/<int:pk>', DetailCategory.as_view(), name="detailcategory"),

    # Orders CRUD
    path('orders/', ListOrders.as_view(), name="orders"),
    path('orders/add/', Checkout.as_view(), name="checkout"),
    path('orders/<int:pk>', DetailOrder.as_view(), name="detailorder"),
    path('orders/edit/<int:pk>', EditOrder.as_view(), name="editorder"),
    path('orders/delete/<int:pk>', DeleteOrder.as_view(), name="deleteorder"),

    # Add review
    path('addreview/', AddReview.as_view(), name="addreview"),

    # Authentication
    path('auth/listusers/', ListUsers.as_view(), name="listusers"),
    path('auth/registration/', UserAuth.as_view(), name='regestration'),
    path('auth/profile/<int:pk>', MyProfile.as_view(), name="myprofile"),
    path('auth/validate/<int:pk>', Validate.as_view(), name="validate"),
    path('auth/login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    # Social Auth
    path('auth/google/', GoogleSocialAuthView.as_view()),
    path('auth/social/facebook/', FacebookSocialAuthView.as_view()),
]
