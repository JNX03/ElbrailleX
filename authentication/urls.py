from django.urls import path
from . import views 
from . import FaceKNN
from django.contrib import admin
from .views import train , save_audio , process_photo , save_image , recognize

urlpatterns = [
    path("login/",views.login, name="login"),
    path("portals",views.portals, name="portals"),
    path('process_photo', views.process_photo, name='process_photo'),
    path('KNN_response', FaceKNN.KNN_response, name='KNN_responses'),
    path("home/", views.home, name="home"),
    path('admin/', admin.site.urls),
    path('train', train, name='train'),
    path('recognize/', recognize, name='recognize'),
    path('', views.welcome_page, name='welcome_page'),
    path('login.html', views.tab_action_page, name='tab_action_page'),
    path('signup.html', views.h_page, name='h_page'),
    path('process_photo/', views.process_photo, name='process_photo'),
    path('saveAudio/', save_audio, name='save_audio'),
    path('saveImage/', save_image, name='save_image'),
]