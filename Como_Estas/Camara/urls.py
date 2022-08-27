from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('testCamara/', views.testCamara, name='testCamara'),

]
