

#include <Servo.h>

//mg996r 모터는 90도 기준으로 0 이면 반시계 회전, 90이상이면 시계방향 회전
//각도 120넘어가면 이상해짐 
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;
void setup() {
  // put your setup code here, to run once:q
  // arduino - motor 연결
  motor1.attach(6); //pin number 입력
  //motor2.attach(9);
  //motor3.attach(10); 
 // motor4.attach(11);
  motor1.write(60);
  Serial.begin(9600);
}
int angles=0;
String receivedString;
void loop() {
  
  if (Serial.available()>0){
    receivedString = Serial.readStringUntil('\n');
    
    //char *ptr = strtok(const_cast<char*>(receivedString.c_str()), ",\n"); // 쉼표 또는 개행 문자로 문자열 분리
    receivedString.trim();  
    const char* ptr=receivedString.c_str();
    angles = atoi(ptr); // 문자열을 정수로 변환하여 배열에 저장
   // Serial.println(angles);
    motor1.write(angles);
    delay(1000);
    Serial.println("Done");
  }
}
