import RPi.GPIO as GPIO
import time


def switch_pressed_callback(channel):
    print("Switch Pressed!")
    
switch_pin = 17

# GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 내부 풀업 저항 활성화
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_pressed_callback, bouncetime=3000)

try:
    # 메인 스레드는 여기에서 다른 작업을 수행할 수 있습니다.
    while True:
        # 메인 루프의 작업을 여기에 넣습니다.
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()