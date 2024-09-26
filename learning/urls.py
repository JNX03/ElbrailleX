from django.urls import path
from . import views
from learning import views

urlpatterns = [
  path("smallalphabet/<int:n>", views.smallalphabetlearning, name='smallalphabetlearning'),
  path("bigalphabet/<int:n>", views.bigalphabetlearning, name='bigalphabetlearning'),
  #path("numberlearning/<int:n>", views.numberlearning, name='numberlearning'),
  path('shorten1/', views.shorten1, name='shorten1'),
  path('shorten2/', views.shorten2, name='shorten2'),
  path('mathlearning/', views.mathlearning, name='mathlearning'),
  path('math1/', views.math1, name='math1'),
  path('math2/', views.math2, name='math2'),
  path('math3/', views.math3, name='math3'),

  path('op1/', views.op1, name='op1'),
  path('op2/', views.op2, name='op2'),

  path('opc1/', views.opc1, name='opc1'),
  path('opc2/', views.opc2, name='opc2'),

  path('sym1/', views.sym1, name='sym1'),
  path('sym2/', views.sym2, name='sym2'),
]