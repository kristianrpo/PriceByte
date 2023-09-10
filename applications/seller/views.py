from django.shortcuts import render,redirect
from .models import Seller
from django.db.models.query import QuerySet
from django.views.generic import ListView,DeleteView,CreateView,UpdateView
from applications.product.models import Product,ImagesProduct
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import FormCreateProduct
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
        if len(products_seller)>0:
            return products_seller
        else:
            return []
class DeleteProduct(SuccessMessageMixin,DeleteView):
    model = Product
    template_name = "seller/DeleteProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Successful elimination"

class CreateProduct(SuccessMessageMixin,CreateView):
    form_class = FormCreateProduct
    template_name = "seller/CreateEditProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Successful creation"
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
    success_message = "Successful modification"
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