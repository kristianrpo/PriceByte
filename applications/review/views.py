from django.shortcuts import render, redirect
from .forms import RatingForm
from .models import Rating

def rating_view(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            warranty_rating = form.cleaned_data['warranty_rating']
            price_rating = form.cleaned_data['price_rating']
            quality_rating = form.cleaned_data['quality_rating']
            overall_rating = form.cleaned_data['overall_rating']
            
            # Guardar los valores en la base de datos
            rating = Rating.objects.create(warranty_rating=warranty_rating, price_rating=price_rating, quality_rating=quality_rating, overall_rating=overall_rating)
            
            # Redireccionar a una página de éxito
            return redirect('nombre-de-la-vista-de-exito')
    else:
        form = RatingForm()
    
    return render(request, 'review/create_review.html', {'form': form})