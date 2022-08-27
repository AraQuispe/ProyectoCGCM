
# importacion de modulos

import cv2
import numpy as np

# creamos el objeto de video (camara)
#captura = cv2.VideoCapture('rtsp://admin:XLKAWA@192.168.2.57/video')
captura = cv2.VideoCapture(0)

# Entregamos el rango necesario para detectar el color amarillo en HSV
greenBajo = np.array([22, 93, 0], np.uint8)
greenAlto = np.array([45, 255, 255], np.uint8)

while captura.isOpened():
    # capturamos frame a frame
    (grabbed, frame) = captura.read()
    # si hemos llegado al final del video salimos
    if not grabbed:
        break

    if grabbed:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV, greenBajo, greenAlto)
        # Eliminamos el posible ruido
        kernel_1 = np.ones((10, 10), np.uint8)
        mascara = cv2.erode(mask, kernel_1, iterations=2)
        mascara = cv2.dilate(mascara, kernel_1, iterations=2)

        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

        total = 0
        for c in contornos:
            area = cv2.contourArea(c)
            #print("area", area)
            if area > 1700:
                # aproximacion de contorno
                peri = cv2.arcLength(c, True)  # Perimetro
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # Si la aproximacion tiene 4 vertices correspondera a un rectangulo
                if len(approx) == 4:
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3, cv2.LINE_AA)
                    total += 1

        # 5.Poner texto en imagen
        letrero = 'Plazas: ' + str(total)
        cv2.putText(frame, letrero, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Mostramos imagen
        cv2.imshow("video", frame)
        #cv2.imshow('mascara', mask)
       # cv2.imshow("MascaraFiltrada", mascara)

        # capturamos teclado
        tecla = cv2.waitKey(25) & 0xFF
        # Salimos si la tecla presionada es ESC
        if tecla == 27:
            break

# Liberamos Objeto
captura.release()

# Destruimos Ventanas
cv2.destroyAllWindows()