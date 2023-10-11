from django.urls import path
from . import views

urlpatterns = [

    path('bar_chart/<str:vendor_name>/', views.bar_chart, name='bar_chart'),
    path('quality/<str:vendor_name>/', views.quality_products, name='quality_products'),
    path('warranty/<str:vendor_name>/', views.warranty_products, name='warranty_products'),

]
