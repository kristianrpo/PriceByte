from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Avg, F, Sum
import spacy
class SearchProducts(TemplateView):
    template_name = "product/search_product.html"

class SearchByNlp(TemplateView):
    template_name = "product/search_product_nlp.html"

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
    paginate_by = 4
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
        
def Search_products_NLP(request):
    template_name = "product/view_product_nlp.html"
    nlp = spacy.load('es_core_news_md')

    top_3_productos = []
    resto_productos = []
    search_by = "Descripción"
    # Si el formulario se envió, recupera la descripción del usuario
    if request.method == 'POST':
        descripcion_usuario = request.POST.get('description', '')
        descripcion_usuario = str(descripcion_usuario.lower())
        
        # Procesa la descripción del usuario
        doc = nlp(descripcion_usuario)
    
        products = Product.objects.all()
        product_info_array = []
        array_info = []

        for product in products:
            product_info_str = (
                f"{product.name_product}\n"
                f"{', '.join(category.name_category for category in product.categories_product.all())}\n"
                f"{product.description_product}\n"
                f"{product.distributed_by_product}\n"
                f"{product.price_product}\n"
            )
            
            product_info_str = str(product_info_str.lower())
            array_info.append(product_info_str) 
            doc_producto = nlp(product_info_str)
            similitud = doc.similarity(doc_producto)
        
            product_info_array.append((product, similitud))

        # Ordenar por similitud de mayor a menor
        productos_ordenados = sorted(product_info_array, key=lambda x: x[1], reverse=True)

        # Obtener los tres productos con mejor similitud
        top_3_productos = [producto[0] for producto in productos_ordenados[:3]]
        resto_productos = [producto[0] for producto in productos_ordenados[3:]]
    return render(request, template_name, {'top_3_productos': top_3_productos, 'resto_productos': resto_productos, 'search_by': search_by})