from django.urls import path
from exercise import views
from . import views
from .views import text_to_speech

urlpatterns = [
    path("practice/<int:n>", views.practice, name='practice'),
    path("alpha1char", views.alphachar, name='alphachar'),
    path('speak/', text_to_speech, name='text_to_speech'),
    path('sort/', views.sort, name='sort'),
    path('sortcoorect/', views.sortcorrect, name='sortt'),
    path('sorttryagain/', views.sorttryagain, name='sorta'),
    path('writing/', views.random, name='random'),
    path('writingawe/', views.randomawe, name='randomawe'),
    path('writingtry/', views.randomtry, name='randomtry'),
]