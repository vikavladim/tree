from django.urls import path
from django.contrib import admin
from . import views
from .signals import generate_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
] + generate_urlpatterns()
