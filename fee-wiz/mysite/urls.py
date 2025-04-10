from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('dj_rest_auth.urls')),
    path('',include('ussd.urls')),
]
