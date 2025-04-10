from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('',views.ussd_callback,name = 'main'),
    # path('user/',api.CreateUser.as_view(),name='create'),
    path('user/',api.userProfile,name='profile'),
    path('create/',api.create_student,name='create'),
    path('callback/',views.mpesacallback,name='callback'),
    path('students/',api.StudentsList.as_view(),name='students'),
    path('transactions/',api.TransactionView.as_view(),name="transactions")
]
