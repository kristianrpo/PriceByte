from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse

def create_client(request, username, email):
    if request.method == 'POST':
        email_client = email
        Name = username

        client = client(email_client = email_client, Name = Name)
        client.save()
       
        return redirect('home')
    
    return render(request, 'seller/create_seller.html')