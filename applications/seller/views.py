from django.shortcuts import render,redirect
from typing import Any, Dict
from .models import Seller
from django.db.models.query import QuerySet
from django.views.generic import ListView,DeleteView,CreateView,UpdateView
from applications.product.models import Product,ImagesProduct
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import FormCreateProduct
from applications.notification.models import Notification
from applications.review.models import ProductRating
from django.db.models import Avg, F, Func, Value, IntegerField,DecimalField
class SellerView(SuccessMessageMixin,ListView):
    model = Product
    template_name = "seller/HomeSeller.html"
    context_object_name = "products"
    paginate_by = 3
    def get_queryset(self):
        seller_1 = self.request.user
        seller_2 = Seller.objects.get(name_company_seller=seller_1)
        searched_product = self.request.GET.get("product",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        products_seller = list_products.filter(distributed_by_product=seller_2)

        products_with_unread_notifications = []
        for product in products_seller:
            unread_notifications_count = Notification.objects.filter(
                seller=seller_2,
                message__icontains=product.name_product,
                is_read=False
            ).count()
            product.unread_notifications_count = unread_notifications_count
            products_with_unread_notifications.append(product)

        if len(products_with_unread_notifications)>0:
            return products_with_unread_notifications
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
        return context
class DeleteProduct(SuccessMessageMixin,DeleteView):
    model = Product
    template_name = "seller/DeleteProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Eliminación exitosa"

class CreateProduct(SuccessMessageMixin,CreateView):
    form_class = FormCreateProduct
    template_name = "seller/CreateEditProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Creación exitosa"
    def form_valid(self, form):
        if self.request.method == 'POST':
            seller_1 = self.request.user
            seller_2 = Seller.objects.get(name_company_seller=seller_1)
            object = form.save(commit=False)
            object.distributed_by_product = seller_2
            object.save()
            for image in self.request.FILES.getlist('image_product'):
                instance = ImagesProduct.objects.create(images_product=image)
                object.image_product.add(instance)
            return super().form_valid(form)

class UpdateProduct(SuccessMessageMixin,UpdateView):
    model = Product
    form_class = FormCreateProduct
    template_name = "seller/CreateEditProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Modificación exitosa"
    def form_valid(self, form):
        if self.request.method == 'POST':
            delete_image_ids = self.request.POST.getlist('delete_images')
            for image_id in delete_image_ids:
                try:
                    image = ImagesProduct.objects.get(id=image_id)
                    image.delete()
                except ImagesProduct.DoesNotExist:
                    pass
            seller_1 = self.request.user
            seller_2 = Seller.objects.get(name_company_seller=seller_1)
            object = form.save(commit=False)
            object.distributed_by_product = seller_2
            object.save()
            for image in self.request.FILES.getlist('image_product'):
                instance = ImagesProduct.objects.create(images_product=image)
                object.image_product.add(instance)
            return super().form_valid(form)

def create_seller(request, username, email):
    if request.method == 'POST':
        NIT_seller = request.POST['NIT_seller']
        name_company_seller = username
        email_seller = email
        phone_number_seller = request.POST['phone_number_seller']
        address = request.POST['address']
        local_number_seller = request.POST['local_number_seller']
        seller = Seller(NIT_seller = NIT_seller, name_company_seller = name_company_seller, email_seller= email_seller,  phone_number_seller = phone_number_seller, address = address, local_number_seller = local_number_seller)
        seller.save()
        return redirect('seller_app:home_seller')
    return render(request, 'seller/create_seller.html')