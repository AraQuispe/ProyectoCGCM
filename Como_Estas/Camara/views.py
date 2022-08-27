from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse

#########################################
from django.views.decorators import gzip
#import cv2
#import threading
from Camara.Code import VideoCamara as vc
#########################################

def inicio(request):
    return render(request,'inicio.html')


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
