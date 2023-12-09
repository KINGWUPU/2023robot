# -*- coding: utf-8 -*-
import time

import adafruit_pca9685


#PWM 드라이버 사용을 위한 객체 생성
robot_handle=adafruit_pca9685.PCA9685()
servoMin = 150 #서보모터 동작 최소 pulse 값
servoMax = 550 #서보모터 동작 최대 pulse 값

#서보모터 동작 각도와 pulse값을 매핑시켜 주기위한 함수
def map(value,min_angle, max_angle, min_pulse, max_pulse):
    angle_range = max_angle-min_angle
    pulse_range = max_pulse-min_pulse
    scale_factor = float(angle_range)/float(pulse_range)
    return min_pulse+(value/scale_factor)

#서보모터 각도 이동을 위한 함수
def set_angle(channel, angle):
    pulse = int(map(angle,0,180,servoMin,servoMax))
    robot_handle.set_pwm(channel,0,pulse)
    
#주파수를 50hz로 지정
robot_handle.set_pwm_freq(50)

while True:
    set_angle(0,10)
    time.sleep(1)
    set_angle(0,90)
    time.sleep(1)