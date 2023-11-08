from typing import Any, Dict
import csv
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView, CreateView
from django.shortcuts import render, get_object_or_404
from .models import Product, Favorite
from applications.review.models import ProductRating
from django.db.models import Avg, F, Func, Value, IntegerField,DecimalField
import spacy
from applications.seller.models import Seller
from .models import ImagesProduct, Category 
from applications.seller.models import Seller
from applications.user.models import Client
from applications.notification.models import Notification
from django.urls import reverse_lazy
from .forms import form_favorite, TuFormulario
from django.shortcuts import get_object_or_404
from applications.accounts.models import User
from applications.seller.models import Seller
from django.shortcuts import redirect

class SearchProducts(TemplateView):
    template_name = "product/search_product.html"

    def get(self, request, *args, **kwargs):
        # Redirige a 'product/recommendations/' cuando se accede a 'product/'
        return redirect('product_app:product_recommendations')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'type'):
            if self.request.user.type == "vendedor":
                context['is_seller'] = "Si"
            else:
                context['is_seller'] = "No"
        else:
            context['is_seller'] = "No"
        return context
    
class SearchByNlp(TemplateView):
    template_name = "product/search_product_nlp.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'type'):
            if self.request.user.type == "vendedor":
                context['is_seller'] = "Si"
            else:
                context['is_seller'] = "No"
        else:
            context['is_seller'] = "No"
        return context

class DetailProduct(DetailView):
    model = Product
    template_name = "product/detail_product.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            list_products1 = Favorite.objects.filter(user=self.request.user)
            lista_nombres = [product.product.name_product for product in list_products1]
            context['list_products_favorites'] = Product.objects.filter(name_product__in=lista_nombres)
        if self.request.user.is_authenticated and Seller.objects.filter(name_company_seller__icontains = self.request.user):
            seller_name = Seller.objects.get(name_company_seller = self.request.user)
            notifications = Notification.objects.filter(
                seller=seller_name,
                message__icontains=self.object.name_product,
                is_read=False
            )
            for notification in notifications:
                notification.is_read = True
                notification.save()

        context['comments'] = ProductRating.objects.all()
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
        )
        list_products = list_products.annotate(
            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
        )
        for product in list_products:
            if product.avg_price_rating != None and product.avg_quality_rating != None and product.avg_warranty_rating != None:
                product.avg_price_rating = round(product.avg_price_rating, 1)
                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                product.total_avg_rating = round(product.total_avg_rating, 1)
            else:
                product.total_avg_rating = "Sin reseñas"
        context["average_products"] = list_products

        if hasattr(self.request.user, 'type'):
            if self.request.user.type == "vendedor":
                context['is_seller'] = "Si"
            else:
                context['is_seller'] = "No"
        else:
            context['is_seller'] = "No"
        return context

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
            list_products = list_products.order_by('-total_avg_rating')
        if option == "recomendación pricebyte":
            weight_price = 0.5
            weight_rating = 0.7
            list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
            )
            list_products = list_products.annotate(
                total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
            )
            list_products = list_products.annotate(
                recommendation_pricebyte = ((F('total_avg_rating'))*weight_rating)/(F('price_product')*weight_price)
            )
            for product in list_products:
                print(f"Producto: {product.name_product}, Promedio: {product.recommendation_pricebyte}")
            list_products = list_products.order_by('-recommendation_pricebyte')
        if len(list_products)>0:
            return list_products
        else:
            return []
    def get_context_data(self, **kwargs: Any):
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        context = super().get_context_data(**kwargs)
        context['search_by'] = option
        if context['search_by'] == "recomendación pricebyte":
            context['search_by'] = "recomendación"
        context['searched_product'] = searched_product
        
        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
        )
        list_products = list_products.annotate(
            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
        )
        for product in list_products:
            if product.avg_price_rating != None and product.avg_quality_rating != None and product.avg_warranty_rating != None:
                product.avg_price_rating = round(product.avg_price_rating, 1)
                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                product.total_avg_rating = round(product.total_avg_rating, 1)
            else:
                product.total_avg_rating = "Sin reseñas"
        context["average_products"] = list_products

        if hasattr(self.request.user, 'type'):
            if self.request.user.type == "vendedor":
                context['is_seller'] = "Si"
            else:
                context['is_seller'] = "No"
        else:
            context['is_seller'] = "No"
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
        if option == "valoración":
            list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
            )
            list_products = list_products.annotate(
                total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
            )
            list_products = list_products.order_by('-total_avg_rating')
        if option == "recomendación pricebyte":
            weight_price = 0.5
            weight_rating = 0.7
            list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
            )
            list_products = list_products.annotate(
                total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
            )
            list_products = list_products.annotate(
                recommendation_pricebyte = ((F('total_avg_rating'))*weight_rating)/(F('price_product')*weight_price)
            )
            for product in list_products:
                print(f"Producto: {product.name_product}, Promedio: {product.recommendation_pricebyte}")
            list_products = list_products.order_by('-recommendation_pricebyte')
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

        searched_product = self.request.GET.get("product",'')
        option = self.request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
        )

        list_products = list_products.annotate(
            total_avg_rating= (F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
        )
        for product in list_products:
            if product.avg_price_rating != None and product.avg_quality_rating != None and product.avg_warranty_rating != None:
                product.avg_price_rating = round(product.avg_price_rating, 1)
                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                product.total_avg_rating = round(product.total_avg_rating, 1)
            else:
                product.total_avg_rating = "Sin reseñas"
        context["average_products"] = list_products

        if hasattr(self.request.user, 'type'):
            if self.request.user.type == "vendedor":
                context['is_seller'] = "Si"
            else:
                context['is_seller'] = "No"
        else:
            context['is_seller'] = "No"
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

        ## rating
        searched_product = request.GET.get("product",'')
        option = request.GET.get("option",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
        )

        list_products = list_products.annotate(
            total_avg_rating= (F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
        )
        for product in list_products:
            if product.avg_price_rating != None and product.avg_quality_rating != None and product.avg_warranty_rating != None:
                product.avg_price_rating = round(product.avg_price_rating, 1)
                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                product.total_avg_rating = round(product.total_avg_rating, 1)
            else:
                product.total_avg_rating = "Sin reseñas"
        if hasattr(request.user, 'type'):
            if request.user.type == "vendedor":
                is_seller = "Si"
            else:
                is_seller = "No"
        else:
            is_seller = "No"
    return render(request, template_name, {'top_3_productos': top_3_productos, 'resto_productos': resto_productos, 'search_by': search_by,'average_products':list_products, 'is_seller': is_seller})


class Confirm_favorite(CreateView):
    form_class = form_favorite
    template_name = "product/confirm_favorite.html"
    success_url = ('product_app:detail_product')

    def form_valid (self, form):
        if self.request.method == 'POST':
            temp_user = self.request.user
            user_real = Client.objects.get(Name = temp_user)
            
            product = self.kwargs['pk']

            print(product)

            product_real = Product.objects.get(id = product)

            Favorite.objects.create(
                user = temp_user,
                product = product_real
            )

        
        return super().form_valid(form)
    
    def get_success_url(self):
        
        return self.request.GET.get('next', reverse_lazy('product_app:search_product'))
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product = self.kwargs['pk']
        temp_user = self.request.user
        kwargs['initial'] = {'user': temp_user, 'product': Product.objects.get(id = product)}
        return kwargs

        

class Favorites(ListView):
    model = Favorite, Product
    template_name = "product/view_favorites.html"
    context_object_name = "product"
    paginate_by = 4

    def get_queryset(self):
        searched_product = self.request.GET.get("product", '')
        option = self.request.GET.get("option", '')
        list_products1 = Favorite.objects.filter(user=self.request.user)

        lista_nombres = []

        for product in list_products1:
            lista_nombres.append(product.product.name_product)
        
        

        list_products = Product.objects.filter(name_product__in=lista_nombres)
        print(list_products)

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
            list_products = list_products.order_by('-total_avg_rating')
        if option == "recomendación pricebyte":
            weight_price = 0.5
            weight_rating = 0.7
            list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
            )
            list_products = list_products.annotate(
                total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
            )
            list_products = list_products.annotate(
                recommendation_pricebyte = ((F('total_avg_rating'))*weight_rating)/(F('price_product')*weight_price)
            )
            for product in list_products:
                print(f"Producto: {product.name_product}, Promedio: {product.recommendation_pricebyte}")
            list_products = list_products.order_by('-recommendation_pricebyte')
        if len(list_products)>0:
            return list_products
        else:
            return []


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        option = self.request.GET.get("option", '')
        context['search_by'] = option

        list_products1 = Favorite.objects.filter(user=self.request.user)

        lista_nombres = []

        for product in list_products1:
            lista_nombres.append(product.product.name_product)
        
        

        list_products = Product.objects.filter(name_product__in=lista_nombres)
        list_products = list_products.annotate(
            avg_price_rating=Avg('productrating__price_rating'),
            avg_quality_rating=Avg('productrating__quality_rating'),
            avg_warranty_rating=Avg('productrating__warranty_rating')
            )
        list_products = list_products.annotate(
            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
        )
        for product in list_products:
            if product.avg_price_rating is not None and product.avg_quality_rating is not None and product.avg_warranty_rating is not None:
                product.avg_price_rating = round(product.avg_price_rating, 1)
                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                product.total_avg_rating = round(product.total_avg_rating, 1)
            else:
                product.total_avg_rating = "Sin reseñas"
        context["average_products"] = list_products

        if hasattr(self.request.user, 'type'):
            context['is_seller'] = "Si" if self.request.user.type == "vendedor" else "No"
        else:
            context['is_seller'] = "No"

        return context
    
from collections import defaultdict


class Recomendations(ListView):
    model = Favorite, Product
    template_name = "product/search_product.html"
    context_object_name = "product"
    paginate_by = 4

    def get_queryset(self):

        if self.request.user.is_authenticated:
            list_products1 = Favorite.objects.filter(user=self.request.user)

            if list_products1.exists():
                lista_nombres = []

                for product in list_products1:
                    lista_nombres.append(product.product.name_product)

                if lista_nombres:  
                    list_products = Product.objects.filter(name_product__in=lista_nombres)
            

            
                    if list_products.exists():
                        unique_categories = set() 
                        category_count = defaultdict(int)
                        selected_products = []

                        for product in list_products:
                            categories_of_product = product.categories_product.all()
                            unique_categories.update(categories_of_product)

                        
                        for category in unique_categories:
                            print(category.name_category)

                        filtered_products = Product.objects.filter(categories_product__in=unique_categories).distinct()

                        print("----------3-------------")
            
                        weight_price = 0.5
                        weight_rating = 0.7
                        filtered_products = filtered_products.annotate(
                        avg_price_rating=Avg('productrating__price_rating'),
                        avg_quality_rating=Avg('productrating__quality_rating'),
                        avg_warranty_rating=Avg('productrating__warranty_rating')
                        )
                        filtered_products = filtered_products.annotate(
                            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
                        )
                        filtered_products = filtered_products.annotate(
                            recommendation_pricebyte = ((F('total_avg_rating'))*weight_rating)/(F('price_product')*weight_price)
                        )

                        for product in filtered_products:
                            print(f"Product: {product.name_product}, Categories: {[category.name_category for category in product.categories_product.all()]}")

                        for product in filtered_products:
                            categories_of_product = product.categories_product.all()

                            if (
                                category_count[product.categories_product.first().id] < 2
                                and product not in list_products
                            ):
                                selected_products.append(product)
                                category_count[product.categories_product.first().id] += 1

                        
                        print("------------4--------------")

                        lista_names =[]
                        for product in selected_products:
                            lista_names.append(product.name_product)
                        
                    
                        list_products_recomended = Product.objects.filter(name_product__in=lista_names)
                        

                

                        list_products_recomended = list_products_recomended.annotate(
                            avg_price_rating=Avg('productrating__price_rating'),
                            avg_quality_rating=Avg('productrating__quality_rating'),
                            avg_warranty_rating=Avg('productrating__warranty_rating')
                            )
                        list_products_recomended = list_products_recomended.annotate(
                            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
                        )
                        
                        for product in list_products_recomended:
                            if product.avg_price_rating is not None and product.avg_quality_rating is not None and product.avg_warranty_rating is not None:
                                product.avg_price_rating = round(product.avg_price_rating, 1)
                                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                                product.total_avg_rating = round(product.total_avg_rating, 1)
                            else:
                                product.total_avg_rating = "Sin reseñas"
                        

                        print(list_products_recomended)
                        print(list_products)

                        for product in list_products_recomended:
                            print(f"Product: {product.name_product}, Categories: {[category.name_category for category in product.categories_product.all()]}")
                        
                        return list_products_recomended

        
        return []


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(f'Contexto: {context}')

        option = self.request.GET.get("option", '')
        context['search_by'] = option

        if self.request.user.is_authenticated:
            list_products1 = Favorite.objects.filter(user=self.request.user)

            if list_products1.exists():
                lista_nombres = []

                for product in list_products1:
                    lista_nombres.append(product.product.name_product)

                if lista_nombres:  
                    list_products = Product.objects.filter(name_product__in=lista_nombres)
            

            
                    if list_products.exists():
                        unique_categories = set() 
                        category_count = defaultdict(int)
                        selected_products = []

                        for product in list_products:
                            categories_of_product = product.categories_product.all()
                            unique_categories.update(categories_of_product)

                        
                        for category in unique_categories:
                            print(category.name_category)

                        filtered_products = Product.objects.filter(categories_product__in=unique_categories).distinct()

                        print("----------3-------------")
            
                        weight_price = 0.5
                        weight_rating = 0.7
                        filtered_products = filtered_products.annotate(
                        avg_price_rating=Avg('productrating__price_rating'),
                        avg_quality_rating=Avg('productrating__quality_rating'),
                        avg_warranty_rating=Avg('productrating__warranty_rating')
                        )
                        filtered_products = filtered_products.annotate(
                            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
                        )
                        filtered_products = filtered_products.annotate(
                            recommendation_pricebyte = ((F('total_avg_rating'))*weight_rating)/(F('price_product')*weight_price)
                        )

                        for product in filtered_products:
                            print(f"Product: {product.name_product}, Categories: {[category.name_category for category in product.categories_product.all()]}")

                        for product in filtered_products:
                            categories_of_product = product.categories_product.all()

                            if (
                                category_count[product.categories_product.first().id] < 2
                                and product not in list_products
                            ):
                                selected_products.append(product)
                                category_count[product.categories_product.first().id] += 1

                        
                        print("------------4--------------")

                        lista_names =[]
                        for product in selected_products:
                            lista_names.append(product.name_product)
                        
                    
                        list_products_recomended = Product.objects.filter(name_product__in=lista_names)
                        

                

                        list_products_recomended = list_products_recomended.annotate(
                            avg_price_rating=Avg('productrating__price_rating'),
                            avg_quality_rating=Avg('productrating__quality_rating'),
                            avg_warranty_rating=Avg('productrating__warranty_rating')
                            )
                        list_products_recomended = list_products_recomended.annotate(
                            total_avg_rating=(F('avg_price_rating') + F('avg_quality_rating') + F('avg_warranty_rating')) / 3
                        )
                        
                        for product in list_products_recomended:
                            if product.avg_price_rating is not None and product.avg_quality_rating is not None and product.avg_warranty_rating is not None:
                                product.avg_price_rating = round(product.avg_price_rating, 1)
                                product.avg_quality_rating = round(product.avg_quality_rating, 1)
                                product.avg_warranty_rating = round(product.avg_warranty_rating, 1)
                                product.total_avg_rating = round(product.total_avg_rating, 1)
                            else:
                                product.total_avg_rating = "Sin reseñas"
                        

                        print(list_products_recomended)
                        print(list_products)

                        for product in list_products_recomended:
                            print(f"Product: {product.name_product}, Categories: {[category.name_category for category in product.categories_product.all()]}")
                        
                        context["average_products"] = list_products_recomended

                        if hasattr(self.request.user, 'type'):
                            context['is_seller'] = "Si" if self.request.user.type == "vendedor" else "No"
                        else:
                            context['is_seller'] = "No"

                        return context

        if hasattr(self.request.user, 'type'):
            context['is_seller'] = "Si" if self.request.user.type == "vendedor" else "No"
        else:
            context['is_seller'] = "No"

        return context
    
def obtener_instancia_seller(usuario_actual):
    
    usuario_seller = get_object_or_404(User, pk=usuario_actual.pk)
    
    seller_instance, creado = Seller.objects.get_or_create(user=usuario_seller)

    return seller_instance


import csv
from django.shortcuts import get_object_or_404
from .models import Product, ImagesProduct, Category, Seller
from applications.accounts.models import User

# ...

# Define la función process_csv aquí
def process_csv(csv_file, seller_instance):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(decoded_file)
    for row in csv_reader:
        name_product, description_product, price_product, quantity_product, code_product, category_name = row

        # Crear una instancia de Product
        product = Product.objects.create(
            name_product=name_product,
            description_product=description_product,
            price_product=price_product,
            quantity_product=quantity_product,
            code_product=code_product,
            distributed_by_product=seller_instance
        )

        # Crear una instancia de ImagesProduct por defecto si no hay imágenes
        if not product.image_product.exists():
            default_image = ImagesProduct.objects.create(images_product='default_image.jpg')
            product.image_product.add(default_image)

        # Crear una instancia de Category si no existe
        category, created = Category.objects.get_or_create(name_category=category_name)
        product.categories_product.add(category)

# ...

# En tu vista principal
def tu_vista(request):
    if request.method == 'POST':
        form = TuFormulario(request.POST, request.FILES)

        # Resto del código para procesar el formulario
        if form.is_valid():
            # Obtener la instancia de Seller asociada al usuario actual
            seller_instance = obtener_instancia_seller(request.user)

            # Guardar el formulario y obtener la instancia de Product
            product = form.save(commit=False)

            # Asignar la instancia de Seller al producto
            product.distributed_by_product = seller_instance

            # Guardar el producto en la base de datos
            product.save()

            # Procesar el archivo CSV si se proporciona
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                # Pasar la instancia de Seller a process_csv
                process_csv(csv_file, seller_instance)

            # Resto del código si es necesario
    else:
        form = TuFormulario()

    return render(request, 'tu_template.html', {'form': form})
