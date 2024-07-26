from django.urls import path
from .views import *

urlpatterns = [
    path('category/', create_category, name='create_category'),
    path('family/', create_family, name='create_family'),
    path('api/items/', create_item, name='create_item'),
    path('customers/', create_customer, name='create_customer')

]
