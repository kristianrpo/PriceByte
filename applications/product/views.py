from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Avg, F, Sum
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
        print(option)
        if option == "precio":
            list_products = list_products.order_by('price_product')
        if option == "valoración":
            list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
        )
            list_products = list_products.annotate(
                total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
            )
            for product in list_products:
                print(f"Producto: {product.name_product}, Promedio: {product.total_avg_rating}")
            list_products = list_products.order_by('-total_avg_rating')
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
        if option == "precio":
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
        
