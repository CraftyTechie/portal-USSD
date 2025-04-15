from django.urls import path
from . import views
from django.contrib import admin
from .views import mpesa_callback
urlpatterns = [
    
    path("home/",views.home),
  

    path("mpesa/callback", views.mpesa_callback, name="mpesa_callback"),
  

]
