from django.urls import path
from .views import SellerView,DeleteProduct,CreateProduct,UpdateProduct,create_seller
app_name = "seller_app"
urlpatterns = [
    path('create_seller/<str:username>/<str:email>/', create_seller, name='create_seller'),
    path('seller/',SellerView.as_view(), name = "home_seller"),
    path('seller/delete/<pk>', DeleteProduct.as_view(), name = "delete_product"),
    path('seller/create', CreateProduct.as_view(),name = "create_product"),
    path('seller/edit/<pk>',UpdateProduct.as_view(),name = "update_product")
]