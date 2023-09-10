from django.urls import path
from . import views
urlpatterns = [        
    path('accounts/signupaccount/', views.signupaccount, name='signupaccount'),
    path('accounts/logout/', views.logoutaccount, name='logoutaccount'),
    path('accounts/login/', views.loginaccount, name='loginaccount'),
    path('', views.home, name='home'),
]