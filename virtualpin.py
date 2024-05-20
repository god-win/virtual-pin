import cv2
import mediapipe as mp
import keyboard as kb
import imutils
import time as t
l=[]
WINDOW_NAME="window" 
FRAME_WIDTH  = 1280
FRAME_HEIGHT =  920
m=[]
i=1
 
THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
Z_THRESHOLD_PRESS = 1
 
VK = {
    '1': { 'x':150+30, 'y':100, 'w':100, 'h':100 },
    '2': { 'x':350+40, 'y':100, 'w':100, 'h':100 },
    '3': { 'x':550+50, 'y':100, 'w':100, 'h':100 },
    '4': { 'x':150+30, 'y':250, 'w':100, 'h':100 },
    '5': { 'x':350+40, 'y':250, 'w':100, 'h':100 },
    '6': { 'x':550+50, 'y':250, 'w':100, 'h':100 },
    '7': { 'x':150+30, 'y':400, 'w':100, 'h':100 },
    '8': { 'x':350+40, 'y':400, 'w':100, 'h':100 },
    '9': { 'x':550+50, 'y':400, 'w':100, 'h':100 },
    '0': { 'x':350+40, 'y':550, 'w':100, 'h':100 }
} 
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
def draw(img, x, y, z,):
    global i
    c=0
    for k in VK:
        if ((VK[k]['x'] < x < VK[k]['x']+VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y']+VK[k]['h']) and (z <= Z_THRESHOLD_PRESS)):
            if i==1:
                if k not in l and k  not in m:
                    if ((VK[k]['x'] < x < VK[k]['x']+VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y']+VK[k]['h']) and (z <= Z_THRESHOLD_PRESS)):
                        cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x']+VK[k]['w'], VK[k]['y']+VK[k]['h']), (0,0,255), -1) 
                        cv2.putText(img, f"{k}", (VK[k]['x']+20,VK[k]['y']+70),cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0), 5, cv2.LINE_AA)
                        l.append(k)
                        
            if i==2:
                if k  not in m:
                    if ((VK[k]['x'] < x < VK[k]['x']+VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y']+VK[k]['h']) and (z <= Z_THRESHOLD_PRESS)):
                        cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x']+VK[k]['w'], VK[k]['y']+VK[k]['h']), (0,0,255), -1) 
                        cv2.putText(img, f"{k}", (VK[k]['x']+20,VK[k]['y']+70),cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0), 5, cv2.LINE_AA)
                        m.append(k)
        else:
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x']+VK[k]['w'], VK[k]['y']+VK[k]['h']), (0,255,0), 1) 
            cv2.putText(img, f"{k}", (VK[k]['x']+20,VK[k]['y']+70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 4, cv2.LINE_AA)
 
def GODH():
    global i
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img=imutils.resize(img,width=1350)
        img = cv2.flip(img, 1)
        if i==1:
            cv2.putText(img,"HI,GODWIN...",(910,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
            cv2.putText(img,"ENTER",(580,600),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,25,255),2)
            cv2.putText(img,"SET YOUR PIN",(200,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        if i==2:
            cv2.putText(img,"ENTER",(580,600),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,25,255),2)
            cv2.putText(img,"ENTER PIN",(300,80),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2)
            cv2.putText(img,"CANCEL",(180,600),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),2)
        if i==3:
            if m==l:
                cv2.putText(img,"SUCCESSFULLY MATCHED",(150,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                cv2.putText(img,"HOW ARE YOU...",(840,320),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                cv2.putText(img,"GODWIN",(910,400),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                if kb.is_pressed("shift"):
                    i=1
                else:
                    i=3
            else:
                cv2.putText(img,"NOT MATCHED",(200,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                cv2.putText(img,"TRY AGAIN",(850,320),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                cv2.putText(img,"PLEASE....",(900,400),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                m.clear()
                if kb.is_pressed("shift"):
                    i=2
                else:
                    i=3
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
 
        x = 0
        y = 0
        z = 0
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) 
                try:
                    index_finger_tip = handLms.landmark[INDEX_FINGER_TIP]
                    x = int(index_finger_tip.x * FRAME_WIDTH)
                    y = int(index_finger_tip.y * FRAME_HEIGHT)
                    z = int(index_finger_tip.z * FRAME_WIDTH)
                    if (z <= Z_THRESHOLD_PRESS):
                        color = (0,0,255) 
                    else:
                        color = (0,255,0)
                    cv2.putText(img,"G", (x,y), cv2.FONT_HERSHEY_SIMPLEX,1, color, 1)
                except IndexError:
                    index_finger_tip = None
 
        draw(img, x, y, z)
 
        cv2.imshow("Godwin", img)
        if kb.is_pressed("enter"):
            i=i+1
        if kb.is_pressed("ctrl"):
            i=1
            GODH()
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            cv2.destroyAllWindows()
            print(l)
            print(m)
            break

if __name__ == "__main__":
    GODH()
 
