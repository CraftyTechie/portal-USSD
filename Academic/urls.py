from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home),
    path("mpesa/callback", views.mpesa_callback, name="mpesa_callback"),
]
