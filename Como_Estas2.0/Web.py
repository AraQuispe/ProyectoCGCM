# Importamos librerias
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
#
import math
import points_Face as pf

# Creamos la app
app =  Flask(__name__)

# Mostramos el video en RT
def gen_frame():
    
    # Realizamos la Videocaptura
    cap = cv2.VideoCapture(0)
    
    # Empezamos
    while True:
        # Leemos la VideoCaptura
        ret, frame = cap.read()

        # Si tenemos un error
        if not ret:
            break

        else:
            # Correccion de color
            #frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Codificamos nuestro video en Bytes
            suc, encode = cv2.imencode('.jpg', frame)
            frame = encode.tobytes()
        try:
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            #Desactivar Camara
            cap.release()
# Ruta de aplicacion 'principal'
@app.route('/')
def index():
    return render_template('Index.html')
# Ruta del video
@app.route('/video')
def video():
    # Aqui se llama a la funcion funcionalde la camara.
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Ejecutamos la app
if __name__ == "__main__":
    app.run(debug = True)