from django.contrib import admin
from django.urls import path
from TGPB import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('j/', views.success, name='success'),
]