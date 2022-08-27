# Importamos librerias
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
#
import math
import points_Face as pf

###########################################################################

# Creamos nuestra funcion de dibujo
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

# Creamos un objeto donde almacenaremos la malla facial
mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

###########################################################################

# Creamos la app
app =  Flask(__name__)


#points=pf.points()


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
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ###########################################################################
            
            # Observamos los resultados
            resultados = MallaFacial.process(frameRGB)
            
    # Añadiendo codigo --¡?¡?¡?¡?¡            
            py=[]
            lista=[]
            px=[]
            r=5
            t=3            
    # Dejando de añadir codigo --¡?¡?¡?¡?¡
            
            # Si tenemos rostros
            if resultados.multi_face_landmarks:
                # Iteramos
                for rostros in resultados.multi_face_landmarks:
                    # Dibujamos
                    #mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)
            
            
            # Añadiendo codigo --¡?¡?¡?¡?¡
                    # Cambio en MEDIAPIPE
                    mpDibujo.draw_landmarks(frame, rostros, pf.points(), ConfDibu, ConfDibu)
                    
                    for id,puntos in enumerate(rostros.landmark):
                        al,an,c=frame.shape
                        x,y=int(puntos.x*an), int (puntos.y*al)
                        px.append(x)
                        py.append(y)
                        lista.append([id,x,y])
                        
                        if len(lista)==468:
                            # Ceja Derecha
                            x1,y1=lista[65][1:]
                            x2,y2=lista[158][1:]
                            cx,cy=(x1+x2)//2,(y1+y2)//2
                            cv2.line(frame, (x1,y1),(x2,y2),(0,0,0),t)
                            cv2.circle(frame,(x1,y1),r,(0,0,0),cv2.FILLED)
                            cv2.circle(frame,(x2,y2),r,(0,0,0),cv2.FILLED)
                            cv2.circle(frame,(cx,cy),r,(0,0,0),cv2.FILLED)
                            
                            longitud1=math.hypot(x2-x1,y1-y1)
                            
                            # Ceja Izquierda
                            x3,y3=lista[295][1:]
                            x4,y4=lista[385][1:]
                            cx2,cy2=(x3+x4)//2,(y3+y4)//2
                            longitud2=math.hypot(x4-x3,y4-y3)
                            cv2.circle(frame,(cx2,cy2),r,(0,0,0),cv2.FILLED)
                            
                            # Boca Extremos
                            x5,y5=lista[78][1:]
                            x6,y6=lista[308][1:]
                            cx3,cy3=(x5+x6)//2,(y5+y6)//2
                            longitud3=math.hypot(x6-x5,y6-y5)
                            cv2.circle(frame,(cx3,cy3),r,(0,255,0),cv2.FILLED)
                            
                            # Boca Apertura
                            x7,y7=lista[13][1:]
                            x8,y8=lista[14][1:]
                            cx4,cy4=(x7+x8)//2,(y7+y8)//2
                            longitud4=math.hypot(x8-x7,y8-y7)
                            cv2.circle(frame,(cx4,cy4),r,(0,0,0),cv2.FILLED)
                            
                            # Clasificacion
                            # Enojado
                            if longitud1<19 and longitud2<19 and longitud3>80 and longitud3<95 and longitud4<5:
                                cv2.putText(frame,'ENOJADO',(480,80),cv2.FONT_HERSHEY_SIMPLEX,1,
                                            (0,0,255),3)
                                #actaulizacion de JS
                            # Feliz
                            if longitud1>20 and longitud1<30 and longitud2>20 and longitud2<30 and longitud3>109 and longitud4>10 and longitud4<20:
                                cv2.putText(frame,'FELIZ',(480,80),cv2.FONT_HERSHEY_SIMPLEX,1,
                                            (0,255,255),3)
                            # Asombrado
                            if longitud1>35 and longitud2>35 and longitud3>80 and longitud3<90 and longitud4>20:
                                cv2.putText(frame,'ASOMBRADO',(480,80),cv2.FONT_HERSHEY_SIMPLEX,1,
                                            (0,255,0),3)
                            # Triste
                            if longitud1>20 and longitud1<35 and longitud2>20 and longitud2<35 and longitud3>80 and longitud3<95 and longitud4<5:
                                cv2.putText(frame,'TRISTE',(480,80),cv2.FONT_HERSHEY_SIMPLEX,1,
                                            (255,0,0),3)   
            # Dejando de añadir codigo --¡?¡?¡?¡?¡
          
           ###########################################################################

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