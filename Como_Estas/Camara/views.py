from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse

#########################################
from django.views.decorators import gzip
#import cv2
#import threading
from Camara.Code import VideoCamara as vc
#########################################

# Create your views here.
def camara(request):
    return HttpResponse("Hola Mundo")

@gzip.gzip_page
def testCamara(request):
    #return render(request,'Camara/index.html')
    ###########################################
    try:
        cam=vc.VideoCamara()
        return StreamingHttpResponse(vc.gen(cam),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request,'Camara/index.html')
    ###########################################

# Uso de variables
def saludo(request,nombre):
    context={'name':nombre}
    return render(request,'Camara/saludo.html',context)

# Uso de condicionales
def moneda(request):
    num=1
    context={'num':num}
    return render(request,'Camara/moneda.html',context)
