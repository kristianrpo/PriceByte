from django.urls import path
from .views import ViewProducts,DetailProduct
app_name = "product_app"
urlpatterns = [
    path('product/', ViewProducts.as_view()),
    path('product/<pk>/',DetailProduct.as_view(), name = "detail_product")
]