from django.db.models.query import QuerySet
from django.views.generic import ListView,DeleteView,CreateView,UpdateView
from .models import Seller
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
        seller = Seller.objects.get(pk=1)
        searched_product = self.request.GET.get("product",'')
        list_products = Product.objects.filter(name_product__icontains = searched_product)
        products_seller = list_products.filter(distributed_by_product=seller)
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
            object = form.save(commit=False)
            object.distributed_by_product = Seller.objects.get(pk=1)
            object.save()
            for image in self.request.FILES.getlist('image_product'):
                instance = ImagesProduct.objects.create(images_product=image)
                object.image_product.add(instance)
            return super().form_valid(form)

class UpdateProduct(UpdateView):
    model = Product
    form_class = FormCreateProduct
    template_name = "seller/CreateEditProduct.html"
    success_url = reverse_lazy('seller_app:home_seller')
    success_message = "Successful creation"
    def form_valid(self, form):
        if self.request.method == 'POST':
            delete_image_ids = self.request.POST.getlist('delete_images')
            for image_id in delete_image_ids:
                try:
                    image = ImagesProduct.objects.get(id=image_id)
                    image.delete()
                except ImagesProduct.DoesNotExist:
                    pass
            object = form.save(commit=False)
            object.distributed_by_product = Seller.objects.get(pk=1)
            object.save()
            for image in self.request.FILES.getlist('image_product'):
                instance = ImagesProduct.objects.create(images_product=image)
                object.image_product.add(instance)
            return super().form_valid(form)





