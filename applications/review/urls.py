from django.urls import path
from . import views

urlpatterns = [        
    path('rating/<pk>/', views.AddReviewView, name='AddReviewView'),

]