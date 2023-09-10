from django.urls import path
from . import views
app_name = "review_app"
urlpatterns = [        
    path('rating/<pk>/', views.AddReviewView, name='AddReviewView'),

]