from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
class ViewProducts(ListView):
    model = Product
    template_name = "product/view_product.html"
    context_object_name = "product"
    def get_queryset(self):
        searched_product = self.request.GET.get("product",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        if len(list_products)>0 and len(searched_product)>0:
            return list_products
        else:
            return []
        
class DetailProduct(DetailView):
    model = Product
    template_name = "product/detail_product.html"
    context_object_name = "product"
