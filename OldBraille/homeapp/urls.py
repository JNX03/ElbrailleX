from django.urls import path
from homeapp import views
from .views import text_to_speech

urlpatterns = [
    path("", views.homescreen, name="homescreen"),
    path("basicbraille/", views.basicbraille, name='basicbraille'),
    path('speak/', text_to_speech, name='text_to_speech'),
    path('index', views.main, name='main'),
]