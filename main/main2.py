import camera
import time
import math
from adafruit_servokit import ServoKit
def control_motor1(yawyaw):
    global angle1
    if yawyaw < -10:
        if angle1>115 :
            return
        angle1=angle1+3
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
    elif yawyaw > 10 :
        if angle1<8 :
            return
        angle1=angle1-3
        kit.servo[0].angle=angle1 
        time.sleep(0.1)
           
    
        
def control_motor3(xx):
    global angle3
    if xx>340:
        if angle3>110 :
            return
        angle3=angle3+3
        kit.servo[6].angle=angle3  
        time.sleep(0.1)
    elif xx<300 :
        if angle3<10 :
            return
        angle3=angle3-3
        kit.servo[6].angle=angle3  
        time.sleep(0.1)           
      
        
def control_motor2(pitchpitch):
    global angle2
    if pitchpitch>30:
        if angle2<15 :
            return
        angle2=angle2-3
        kit.servo[3].angle=angle2 
        time.sleep(0.1)
    elif pitchpitch<-30 :
        if angle2>105 :
            return
        angle2=angle2+3
        kit.servo[3].angle=angle2 
        time.sleep(0.1)        

def control_motor4(rollroll):
    global angle4
    if rollroll<-3 :
        if angle4<5 :
            return
        angle4=angle4-1
        kit.servo[9].angle=angle4 
        time.sleep(0.1)
    elif rollroll>3 :
        if angle4>115 :
            return
        angle4=angle4+1
        kit.servo[9].angle=angle4 
        time.sleep(0.1)        
def setting_dir_pos(roll_pitch_yaw) :
    global roll, pitch, yaw, x, y, img
    roll = roll_pitch_yaw[0]
    pitch = roll_pitch_yaw[1]
    yaw = roll_pitch_yaw[2]
    x=roll_pitch_yaw[3]
    y=roll_pitch_yaw[4]
   # print(roll_pitch_yaw)  
 
            
#set channel
kit = ServoKit(channels=16)
angle1=60
angle2=80
angle3=60
angle4=60
#set initial pos
kit.servo[0].angle=60
kit.servo[3].angle=80
kit.servo[6].angle=60
kit.servo[9].angle=60
time.sleep(3)
global img
img=None

roll_pitch_yaw = camera.capture_axis()

roll = roll_pitch_yaw[0]
pitch = roll_pitch_yaw[1]
yaw = roll_pitch_yaw[2]
x=roll_pitch_yaw[3]
y=roll_pitch_yaw[4]

print(roll_pitch_yaw)

while(1) :
    # jj=input("cap?")
    roll_pitch_yaw = camera.capture_axis()
    # camera.cv2.imshow('img', image)
    setting_dir_pos(roll_pitch_yaw)
    
    if abs(yaw)>10 :
        while (1) :
            # jj=input("before 1")
            start_time = time.time()
            control_motor1(yaw)
            roll_pitch_yaw = camera.capture_axis()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("after move motor1:"+ str(elapsed_time))
            setting_dir_pos(roll_pitch_yaw)
            if abs(x-320)>20 :
                # jj=input("before 3")
                
                start_time = time.time()
                control_motor3(x)
                roll_pitch_yaw = camera.capture_axis()
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("after move motor3:"+ str(elapsed_time))
                setting_dir_pos(roll_pitch_yaw)
            if abs(yaw)<10 and abs(x-320)<20 :
                print('1,3 terminate')
                break
            
            # face tracking fail
            # if abs(yaw)==0 and abs(x)==0:
            #     print('1,3 terminate')
            #     break
            
        if abs(y-240)>30 : 
            while (1):
                 #jj=input("before 2")
                control_motor2(pitch)
                roll_pitch_yaw = camera.capture_axis()
                 #ㅇ
                setting_dir_pos(roll_pitch_yaw)
                if abs(pitch)<30 :
                    print('2 terminate')
                    break
    if abs(roll)>3:
        while (1) :
            control_motor4(roll)
            roll_pitch_yaw = camera.capture_axis()
                #ㅇ
            setting_dir_pos(roll_pitch_yaw)
            if abs(roll)<3 :
                print('4 terminate')
                break
    #print("hi")
    print(roll)        
# cap.release()

