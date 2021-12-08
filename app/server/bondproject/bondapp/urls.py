from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.home_template, name="home"),
    url('test/', views.test, name="test"),
]
