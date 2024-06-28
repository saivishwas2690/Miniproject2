from django.urls import path,include
from .views import *

app_name = 'problems'  

urlpatterns = [
    path('modules/', modules, name='modules'),
    path('test/', test_code, name='test'),
    path('run/', simple_run_code, name='run'),
    path('suggestions/', suggestions, name='suggestions'),
    path('getcode/',getcode, name='getcode'),
    path('<string>/', problems_list, name='problems'),
    path('<string>/<int:pk>/', problem_detail, name='problem_detail'),
]