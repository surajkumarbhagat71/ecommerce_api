from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('register/',Register.as_view(),name="register"),
    path('logout/', Logout.as_view(), name='auth_logout'),

]
