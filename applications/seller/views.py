from django.shortcuts import render, redirect
from .models import Seller

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
        
        # Redirige a donde desees después de crear al vendedor
        return redirect('home')
    
    return render(request, 'seller/create_seller.html')