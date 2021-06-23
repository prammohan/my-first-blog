from typing import Counter
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]





 
