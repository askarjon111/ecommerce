from django.urls import path
from .views import *

urlpatterns = [
    path('', ListProducts.as_view(), name='index'),
    path('add/', AddProduct.as_view(), name='addproduct'),
    path('product/<int:pk>', DetailProduct.as_view(), name="productdetail"),

    path('orderitems/', ListOrderItems.as_view(), name="orderitems"),
    path('addorderitem/', AddOrderItems.as_view(), name='addorders'),
    path('orderitem/<int:pk>', DetailOrderItem.as_view(), name="detailorderitem"),

    path('categories/', ListCategories.as_view(), name="category"),
    path('category/<int:pk>', DetailCategory.as_view(), name="detailcategory"),

    path('orders/', ListOrders.as_view(), name="orders"),
    path('addorder/', AddOrder.as_view(), name="addorder"),
]
