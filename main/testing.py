import mediapipe as mp
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import pickle
import glob
import scipy.io

# dan's library
import serial
import time
import math

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# # load model
# model = pickle.load(open('./model.pkl', 'rb'))

# # setting
# cols = []
# for pos in ['nose_', 'forehead_', 'left_eye_', 'mouth_left_', 'chin_', 'right_eye_', 'mouth_right_']:
#     for dim in ('x', 'y'):
#         cols.append(pos+dim)

# # serial setting
# serial_port='/dev/ttyUSB0' #포트 정보
# baud_rate = 9600 #arduino와 일치 시킬것
# ser = serial.Serial(serial_port,baud_rate)

# angle1=60
# angle2=80
# angle3=60
# angle4=60

### def ###
def extract_features(img, face_mesh):
    NOSE = 1
    FOREHEAD = 10
    LEFT_EYE = 33
    MOUTH_LEFT = 61
    CHIN = 199
    RIGHT_EYE = 263
    MOUTH_RIGHT = 291

    result = face_mesh.process(img)
    face_features = []
    
    if result.multi_face_landmarks != None:
        for face_landmarks in result.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [FOREHEAD, NOSE, MOUTH_LEFT, MOUTH_RIGHT, CHIN, LEFT_EYE, RIGHT_EYE]:
                    face_features.append(lm.x)
                    face_features.append(lm.y)

    return face_features

def normalize(poses_df):
    normalized_df = poses_df.copy()
    
    for dim in ['x', 'y']:
        # Centerning around the nose 
        for feature in ['forehead_'+dim, 'nose_'+dim, 'mouth_left_'+dim, 'mouth_right_'+dim, 'left_eye_'+dim, 'chin_'+dim, 'right_eye_'+dim]:
            normalized_df[feature] = poses_df[feature] - poses_df['nose_'+dim]
        
        
        # Scaling
        diff = normalized_df['mouth_right_'+dim] - normalized_df['left_eye_'+dim]
        for feature in ['forehead_'+dim, 'nose_'+dim, 'mouth_left_'+dim, 'mouth_right_'+dim, 'left_eye_'+dim, 'chin_'+dim, 'right_eye_'+dim]:
            normalized_df[feature] = normalized_df[feature] / diff
    
    return normalized_df

def draw_axes(img, pitch, yaw, roll, tx, ty, size=50):
    yaw = -yaw
    rotation_matrix = cv2.Rodrigues(np.array([pitch, yaw, roll]))[0].astype(np.float64)
    
    # for testing
    # print(rotation_matrix)
    
    axes_points = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
    ], dtype=np.float64)
    axes_points = rotation_matrix @ axes_points
    axes_points = (axes_points[:2, :] * size).astype(int)
    axes_points[0, :] = axes_points[0, :] + tx
    axes_points[1, :] = axes_points[1, :] + ty
    
    new_img = img.copy()
    cv2.line(new_img, tuple(axes_points[:, 3].ravel()), tuple(axes_points[:, 0].ravel()), (255, 0, 0), 3)    
    cv2.line(new_img, tuple(axes_points[:, 3].ravel()), tuple(axes_points[:, 1].ravel()), (0, 255, 0), 3)    
    cv2.line(new_img, tuple(axes_points[:, 3].ravel()), tuple(axes_points[:, 2].ravel()), (0, 0, 255), 3)
    return new_img

### dan's def ###
def control_motor1(yawyaw):
    global angle1,angle2,angle3,angle4
    if yawyaw>10:
        if angle1>115 :
            return
        angle1=angle1+5
    elif yawyaw<-10 :
        if angle1<5 :
            return
        angle1=angle1-5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break
        
def control_motor3(xx):
    global angle1,angle2,angle3,angle4
    if xx>340:
        if angle3>110 :
            return
        angle3=angle3+5
    elif xx<300 :
        if angle3<10 :
            return
        angle3=angle3-5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break    
        
def control_motor2(pitchpitch):
    global angle1,angle2,angle3,angle4
    if pitchpitch>20:
        if angle2<10 :
            return
        angle2=angle2-5
    elif pitchpitch<-20 :
        if angle2>110 :
            return
        angle2=angle2+5
            
    message= str(angle1)+','+str(angle2)+','+str(angle3)+','+str(angle4)
    print(message.encode())
    ser.write(message.encode())
    while(1) :
        received_data=ser.readline().decode().strip() #arduino로 부터 받은 데이터를 개행문자까지 제거하여 저장
        
        print(received_data)
        if received_data=='Done':
            break 

# load model
model = pickle.load(open('./model.pkl', 'rb'))        

# setting
cols = []
for pos in ['nose_', 'forehead_', 'left_eye_', 'mouth_left_', 'chin_', 'right_eye_', 'mouth_right_']:
    for dim in ('x', 'y'):
        cols.append(pos+dim)

# serial setting
serial_port='/dev/ttyUSB0' #포트 정보
baud_rate = 9600 #arduino와 일치 시킬것
ser = serial.Serial(serial_port,baud_rate)

angle1=60
angle2=80
angle3=60
angle4=60
        
face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)  # From Raspi Camera

while(cap.isOpened()):
    # Take each frame
    ret, img = cap.read()
    if ret:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.flip(img, 1)
        img_h, img_w, img_c = img.shape
        text = ''
        
        face_features = extract_features(img, face_mesh)
        if len(face_features):
            face_features_df = pd.DataFrame([face_features], columns=cols)
            face_features_normalized = normalize(face_features_df)
            pitch_pred, yaw_pred, roll_pred = model.predict(face_features_normalized).ravel()
            nose_x = face_features_df['nose_x'].values * img_w
            nose_y = face_features_df['nose_y'].values * img_h
            img = draw_axes(img, pitch_pred, yaw_pred, roll_pred, nose_x, nose_y)
                        
            if pitch_pred > 0.3:
                text = 'Top'
                if yaw_pred > 0.3:
                    text = 'Top Left'
                elif yaw_pred < -0.3:
                    text = 'Top Right'
            elif pitch_pred < -0.3:
                text = 'Bottom'
                if yaw_pred > 0.3:
                    text = 'Bottom Left'
                elif yaw_pred < -0.3:
                    text = 'Bottom Right'
            elif yaw_pred > 0.3:
                text = 'Left'
            elif yaw_pred < -0.3:
                text = 'Right'
            else:
                text = 'Forward'            
            
        if(face_features!=[]):
            
            # change to radian
            roll2 = roll_pred * 57.3
            yaw2 = yaw_pred * 57.3
            pitch2 = pitch_pred * 57.3
            
            cv2.putText(img, text, (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(img, f"Roll: {roll2:.2f}", (25, 105), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, f"Yaw: {yaw2:.2f}", (25, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, f"Pitch: {pitch2:.2f}", (25, 165), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # cv2.putText(img, f"Roll: {roll_pred:.2f}", (25, 105), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.putText(img, f"Yaw: {yaw_pred:.2f}", (25, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.putText(img, f"Pitch: {pitch_pred:.2f}", (25, 165), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(img, f"X: {nose_x[0]:.1f}", (25, 195), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, f"Y: {nose_y[0]:.1f}", (25, 225), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # if(abs(yaw2)>20):
            #     print("move_moter_1_3")
            #     control_motor1(yaw2)
            #     control_motor3(nose_x[0])
            #     if abs(yaw2)<20 and abs(nose_x[0]-320)<40 :
            #         print('stop_motor_1_3')
                
            # if(abs(nose_y[0]-240)>30): 
            #     print("move_motor_2")
            #     control_motor2(pitch2)
            #     if abs(pitch2)<20 :
            #         print('stop_motor_2')
            
            
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # vertical = cv2.flip(img, 1)
        # cv2.imshow('img', img)
        # cv2.imshow('vertical', vertical)
        # print(text)
        # print(nose_x, nose_y)
        
        
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()