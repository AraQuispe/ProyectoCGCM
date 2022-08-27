from django.urls import path

from . import views

urlpatterns = [
    path('', views.camara, name='hola'),
    path('testCamara/', views.testCamara, name='testCamara'),

    # path('<str:nombre>/',views.saludo,name='saludo'),
    path('moneda/', views.moneda, name='moneda'),
]
