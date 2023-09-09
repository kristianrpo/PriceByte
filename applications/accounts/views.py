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
    return render(request, 'home.html')

def signupaccount(request):
    if request.method == 'GET':
        print(18)
        return render(request, 'accounts/signupaccount.html', 
                      {'form':UserCreateForm})            
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
                    print("NO HOLA")
                return redirect('home')
            except IntegrityError:
                return render(request, 'accounts/signupaccount.html', 
                 {'form':UserCreateForm,
                 'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'accounts/signupaccount.html', 
             {'form':UserCreateForm, 'error':'Passwords do not match'})

@login_required
def logoutaccount(request):        
    logout(request)
    return redirect('home')

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'accounts/loginaccount.html', 
                      {'form':AuthenticationForm})            
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])            
        if user is None:                                
            return render(request,'accounts/loginaccount.html', 
                    {'form': AuthenticationForm(), 
                    'error': 'username and password do not match'})
        else: 
            login(request,user)
            return redirect('home')