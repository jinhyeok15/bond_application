from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('home/', views.home_template, name="home"),
]
