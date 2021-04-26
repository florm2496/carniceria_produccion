from django.urls import path , include 
from .views import Home , Dashboard , HomeSinPrivilegios
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',Dashboard  ,name='dashboard'),
    path('home',Home  ,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='bases/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='bases/login.html'),name='logout'),
      #path('dashboard/' , Dashboard , name='dashboard'),
      
    path('sin_privilegios/',HomeSinPrivilegios.as_view(),name='sin_privilegios'),
    #path('dashboard/' , Dashboard , name='dashboard'),
]