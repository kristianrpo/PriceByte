from django.urls import path
from . import views

urlpatterns = [
    path('create_seller/<str:username>/<str:email>/', views.create_seller, name='create_seller'),
]