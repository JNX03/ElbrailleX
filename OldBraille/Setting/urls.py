from django.urls import path
from . import views
from Setting import views

urlpatterns = [
  path("Connect", views.CM, name='Connect'),
  path("TT", views.tt, name='Tt'),
  path("Transalte", views.tran, name='Tran'),
  path('upload/', views.upload_file, name='upload_file'),
  path('upload/success/', views.upload_success, name='file_upload_success'),
  path('files/', views.file_list, name='file_list'),
]