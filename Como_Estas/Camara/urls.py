from django import views
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('testCamara/', views.testCamara, name='testCamara'),

]
