from django.urls import path,include
from .views import *

app_name = 'accounts'  

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginuser, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('advice/', advise, name='advice'),
    
]