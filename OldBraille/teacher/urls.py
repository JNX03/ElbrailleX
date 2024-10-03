from django.urls import path
from homeapp import views
from .views import home

urlpatterns = [
    path("", home, name="home"),
]