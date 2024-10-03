from django.urls import path
from . import views
from Setting import views

urlpatterns = [
  path("Connect", views.CM, name='Connect'),
  path("TT", views.tt, name='Tt'),
]
