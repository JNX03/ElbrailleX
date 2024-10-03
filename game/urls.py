from django.urls import path
from .views import random_letter_view , upper , lower , short ,math2, sym1

urlpatterns = [
    path('', random_letter_view, name='random_letter'),
    path('lower/', lower, name='lower'),
    path('upper/', upper, name='upper'),
    path('short/', short, name='short'),
    path('math2/', math2, name='math2'),
    path('sym1/', sym1, name='sym1'),
]
