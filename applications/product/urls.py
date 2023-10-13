from django.urls import path
from .views import ViewProducts,SearchProducts,ViewAllProducts,DetailProduct, SearchByNlp,Search_products_NLP, Confirm_favorite
app_name = "product_app"
urlpatterns = [
    path('product/', SearchProducts.as_view(),name = "search_product"),
    path('product/<int:pk>/', DetailProduct.as_view(), name='detail_product'),
    path('product/viewproducts',ViewProducts.as_view(), name = "view_product"),
    path('product/view_all_products',ViewAllProducts.as_view(), name = "view_all_products"),
    path('product/search_description', SearchByNlp.as_view(), name = "search_by_nlp"),
    path('product/viewproductsnlp',Search_products_NLP, name = "view_product_nlp"),
    path('product/Confirm_favorite',Confirm_favorite, name = "Add_favorite")
]   