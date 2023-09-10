from django.urls import path
from .views import ViewProducts,SearchProducts,ViewAllProducts,DetailProduct
app_name = "product_app"
urlpatterns = [
    path('product/', SearchProducts.as_view(),name = "search_product"),
    path('product/<int:pk>/', DetailProduct.as_view(), name='detail_product'),
    path('product/viewproducts',ViewProducts.as_view(), name = "view_product"),
    path('product/view_all_products',ViewAllProducts.as_view(), name = "view_all_products")

]