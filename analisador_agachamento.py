

import cv2
import mediapipe as mp
print(mp)
print(mp.__file__)
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def calcular_angulo(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c

    angulo = math.degrees(
        math.atan2(cy - by, cx - bx) -
        math.atan2(ay - by, ax - bx)
    )

    angulo = abs(angulo)

    if angulo > 180:
        angulo = 360 - angulo

    return angulo


cap = cv2.VideoCapture(0)

dados =  [] 
contador = 0
fase = "None"


with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
   
   
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Erro ao acessar a webcam.")
            break

        frame = cv2.flip(frame, 1)
        imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = pose.process(imagem_rgb)

            
            
        if resultado.pose_landmarks:

            landmarks = resultado.pose_landmarks.landmark

            hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]


            if (hip.visibility < 0.7 or knee.visibility < 0.7 or ankle.visibility < 0.7):

                cv2.putText(frame,"Mostre o corpo inteiro", (30, 50),   
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Analisador de Postura - Terminal", frame)

                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break
                
                
                continue

            
              
              
              
              
              
              
              
            altura, largura, _ = frame.shape
            
            
            
            
            
            
            
            
            
            
            
            
            
        

            quadril = [
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * largura,
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * altura
            ]

            joelho = [
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * largura,
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * altura
            ]

            tornozelo = [
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * largura,
                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * altura
            ]

            angulo_joelho = calcular_angulo(quadril, joelho, tornozelo)

            if angulo_joelho < 100:
                status = "AGACHAMENTO CORRETO"
                fase = "agachado"
            elif angulo_joelho < 150:
                status = "QUASE CORRETO"

            else:
                status = "AGACHE MAIS"

            if angulo_joelho > 160 and fase == "agachado":
                fase = "em_pe"
                contador += 1
                
            print(f"Angulo do joelho: {int(angulo_joelho)} | Status: {status}")

            cv2.putText(frame, f"Angulo: {int(angulo_joelho)}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.putText(frame, status, (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame,f"Repeticoes: {contador}", (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            mp_drawing.draw_landmarks(
                frame,
                resultado.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        cv2.imshow("Analisador de Postura - Terminal", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()