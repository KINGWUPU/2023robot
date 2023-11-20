

#include <Servo.h>

//mg996r 모터는 90도 기준으로 0 이면 반시계 회전, 90이상이면 시계방향 회전
//각도 120넘어가면 이상해짐 
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;
void setup() {
  // put your setup code here, to run once:
  // arduino - motor 연결
  motor1.attach(6); //pin number 입력
  //motor2.attach(9);
  //motor3.attach(10); 
 // motor4.attach(11);
}

void loop() {
  // put your main code here, to run repeatedly:
  //각도 입력
  motor1.write(60);
 // motor2.write(60);
  //motor3.write(60);
  //motor4.write(60);
  int j=200;
  delay(1000);
  //속도의 경우 for 문을 통해 제어 가능
  //delay가 10정도면 원래 속도처럼 동작
  for (int theta1=0; theta1<120; theta1++){
    motor1.write(theta1);
    delay(j);
    if (j<20) {
      continue;
    }
    j-=10;
     
  }
}

