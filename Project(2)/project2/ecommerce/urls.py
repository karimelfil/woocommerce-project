from django.urls import path
from .views import create_category

urlpatterns = [
    path('category/', create_category, name='create_category'),
]
