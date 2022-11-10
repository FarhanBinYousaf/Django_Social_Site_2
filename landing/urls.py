from django.urls import path
from .views import UserRegister, Home, Login
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',Home.as_view(),name="index"),
    path('register/',UserRegister.as_view(),name="register"),
    path('login/',auth_views.LoginView.as_view(template_name="landing/login.html"),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name="landing/logout.html"),name="logout"),

]

