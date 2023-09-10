from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductRating
from applications.product.models import Product
from .forms import ProductRating
from applications.accounts.views import loginaccount 

@login_required(login_url= loginaccount) 
def AddReviewView(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form =ProductRating(request.POST)  # Usa un formulario si lo tienes definido
        if form.is_valid():
            # Procesa y guarda los datos del formulario en la base de datos
            price_rating = form.cleaned_data['price_rating']
            quality_rating = form.cleaned_data['quality_rating']
            warranty_rating = form.cleaned_data['warranty_rating']
            description = form.cleaned_data['description']

            ProductRating.objects.create(
                product=product,
                price_rating=price_rating,
                quality_rating=quality_rating,
                warranty_rating=warranty_rating,
                description=description
            )

            # Redirige a la página de detalles del producto
            return redirect('detail_product', pk=pk)
    else:
        form =ProductRating()  # Crea una instancia del formulario vacío

    # Si el método no es POST o el formulario no es válido, muestra el formulario
    context = {'product': product, 'form': form}
    return render(request, 'review/create_review.html', context)
