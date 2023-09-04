from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from .models import Product
class SearchProducts(TemplateView):
    template_name = "product/search_product.html"

class DetailProduct(DetailView):
    model = Product
    template_name = "product/detail_product.html"
    context_object_name = "product"

class ViewProducts(ListView):
    model = Product
    template_name = "product/view_products.html"
    context_object_name = "product"
    def get_queryset(self):
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        if option == "price":
            list_products = list_products.order_by('price_product')
        if len(list_products)>0:
            return list_products
        else:
            return []
    def get_context_data(self, **kwargs: Any):
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        context = super().get_context_data(**kwargs)
        context['search_by'] = option
        context['searched_product'] = searched_product
        return context

class ViewAllProducts(ListView):
    model = Product
    template_name = "product/view_all_products.html"
    context_object_name = "product"
    paginate_by = 1
    def get_queryset(self):
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        if option == "price":
            list_products = list_products.order_by('price_product')
        if len(list_products)>0:
            return list_products
        else:
            return []
    def get_context_data(self, **kwargs: Any):
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        context = super().get_context_data(**kwargs)
        context['search_by'] = option
        context['searched_product'] = searched_product
        return context
        
