from django.urls import path
from .views import *

urlpatterns = [
    path('', ListProducts.as_view(), name='index'),
]
