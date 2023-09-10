from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductRating
from applications.product.models import Product
from .forms import ProductRatingForm
from applications.accounts.views import loginaccount

@login_required(login_url= loginaccount) 
def AddReviewView(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form =ProductRatingForm(request.POST) 

        if form.is_valid():
            username = request.user
            price_rating = form.cleaned_data['price_rating']
            quality_rating = form.cleaned_data['quality_rating']
            warranty_rating = form.cleaned_data['warranty_rating']
            description = form.cleaned_data['description']

            ProductRating.objects.create(
                product=product,
                price_rating=price_rating,
                quality_rating=quality_rating,
                warranty_rating=warranty_rating,
                description=description,
                username = username
            )

            return redirect('product_app:detail_product', pk=pk)
    else:
        form =ProductRating()

    context = {'product': product, 'form': form}
    return render(request, 'review/create_review.html', context)
