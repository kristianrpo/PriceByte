from django.shortcuts import render
from .forms import UserCreateForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from applications.seller.views import *

def home(request):
    if hasattr(request.user, 'type'):
        if request.user.type == "vendedor":
            is_seller = "Si"
        else:
            is_seller = "No"
    else:
        is_seller = "No"
    return render(request, 'home.html',{'is_seller':is_seller})

def signupaccount(request):
    if request.method == 'GET':
        form = UserCreateForm()
        if hasattr(request.user, 'type'):
            if request.user.type == "vendedor":
                is_seller = "Si"
            else:
                is_seller = "No"
        else:
            is_seller = "No"
        return render(request, 'accounts/signupaccount.html', 
                      {'form':form,'is_seller':is_seller})            
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], 
                            password=request.POST['password1'],
                            email=request.POST['email'],
                            type=request.POST['type'])
                user.save()
                login(request, user)
                if(user.type== 'vendedor'):
                    return redirect('seller_app:create_seller', username=user.username, email=user.email)
                else:
                    return redirect('product_app:search_product')
            except IntegrityError:
                if hasattr(request.user, 'type'):
                    if request.user.type == "vendedor":
                        is_seller = "Si"
                    else:
                        is_seller = "No"
                else:
                    is_seller = "No"
                return render(request, 'accounts/signupaccount.html', 
                 {'form':UserCreateForm,
                 'error':'Username already taken. Choose new username.',
                 'is_seller':is_seller,
                 })
        else:
            if hasattr(request.user, 'type'):
                if request.user.type == "vendedor":
                    is_seller = "Si"
                else:
                    is_seller = "No"
            else:
                is_seller = "No"
            return render(request, 'accounts/signupaccount.html', 
             {'form':UserCreateForm, 'error':'Passwords do not match', 'is_seller':is_seller})

@login_required
def logoutaccount(request):        
    logout(request)
    return redirect('product_app:search_product')

def loginaccount(request):
    if request.method == 'GET':
        if hasattr(request.user, 'type'):
            if request.user.type == "vendedor":
                is_seller = "Si"
            else:
                is_seller = "No"
        else:
            is_seller = "No"
        return render(request, 'accounts/loginaccount.html', 
                      {'form':AuthenticationForm, 'is_seller':is_seller})            
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])            
        if user is None:
            if hasattr(request.user, 'type'):
                if request.user.type == "vendedor":
                    is_seller = "Si"
                else:
                    is_seller = "No"
            else:
                is_seller = "No"                                
            return render(request,'accounts/loginaccount.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match',
                    'is_seller':is_seller,
                    })
        else: 
            login(request,user)
            if(user.type  == 'vendedor'):
                return redirect('seller_app:home_seller')
            else:
                return redirect('product_app:search_product')