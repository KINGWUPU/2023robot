import RPi.GPIO as GPIO
import time

switch_pin = 17

# GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 내부 풀업 저항 활성화

try:
    while True:
        if GPIO.input(switch_pin) == False: # 스위치가 눌렸을 때
            print("Switch Pressed")
            # 여기에 원하는 작업을 추가할 수 있습니다.
            time.sleep(0.5) # 디바운싱을 위한 지연
        else:
            # 스위치가 눌리지 않았을 때의 작업
            pass

except KeyboardInterrupt:
    GPIO.cleanup() # 프로그램 종료 시 GPIO 정리