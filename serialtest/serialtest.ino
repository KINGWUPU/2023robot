//Test for controling angles by serial protocal
#include <Servo.h>
#include <math.h>
//declare 4 servo motors.
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

//simple serial tset
//,로 구분된 4가지 정수를 받아들여 값이 배열에 정확히 저장되는지 확인해보는 파일
int current_angles[4]={60,60,60,60};
int dest_angles[4]={60,60,60,60};

//현재각과 목표각의 차이 저장
int dif_angles[4]={0,0,0,0};
void setup() {
  
  motor1.attach(6); //pin number 입력
  motor2.attach(9);
  motor3.attach(10);
  motor4.attach(11);
  //initial angles are 60
  motor1.write(60);
  motor2.write(60);
  motor3.write(60);
  motor4.write(60);
  //board rate 
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available()>0){
    String receivedString = Serial.readStringUntil('\n');
    int index=0;
    char *ptr = strtok(const_cast<char*>(receivedString.c_str()), ",\n"); // 쉼표 또는 개행 문자로 문자열 분리
    while (ptr != NULL && index < 4) {
        dest_angles[index++] = atoi(ptr); // 문자열을 정수로 변환하여 배열에 저장
        ptr = strtok(NULL, ",\n");
      }

    int max_duration=0, min_duration=120; //모터가 가장 크게 움직여야할 각도, 가장 적게 움직여야할 각도를 정함
    //최소로 움직여야할 각, 최대로 움직여야할 각도를 저장
    for (int j=0;j<4;j++) {
      dif_angles[j]=dest_angles[j]-current_angles[j];
      if (max_duration<abs(dif_angles[j])){
          max_duration=abs(dif_angles[j]);
      }

      if (min_duration>abs(dif_angles[j])) {
          min_duration=abs(dif_angles[j]);
      }
    }

    //만약 모터가 움직여야할 최대각도가 0이 아니라면 모터를 움직여야함, 0인 경우는 모터를 움직일 필요가 없음
    if (max_duration!=0) {
        //Serial.println("move!");
        move_angle(max_duration,min_duration);
      //  motor1.write(dest_angles[0]);
      //  motor2.write(dest_angles[1]);
       // motor3.write(dest_angles[2]);
       // motor4.write(dest_angles[3]);
    }
    


    for (int o=0;o<4;o++) {
      current_angles[o]=dest_angles[o];
    }
    Serial.println("Done");
  }


}

/*move motor - 최대로 움직여야할 각과 최소로 움직여야할 각을 받아 모터를 동작
  모터는 속력이 증가, 일정, 감소하는 3구간으로 나누어져 동작, 인자 값은 그 구간을 나누는 기준이 된다.*/
void move_angle(int max, int min){
  int direction[4]; //각 값은 모터가 움직일 각도의 방향을 저장 (-1 or 1)
  int duration; //duration은 각 구간의 크기를 정하는 방향이 됌
  //초기 구간을 설정하는 로직 : min이 0일 경우(움직이지 않는 모터가 있을 경우, 그 구간은 max값을 이용해 결정된다)
 /* if (min==0) {
    duration=max/3;
  }
  //min이 0이 아닐 경우, 그 구간은 min으로 결정된다
  else {
    duration=min;
  }*/
  duration=max/3;
  //모터가 움직일 방향을 정한다, 만약 모터를 움직일 필요가 없다면 방향은 0으로 설정함
  for (int i=0;i<4;i++) {
    
    if (dif_angles[i]==0) {
      direction[i]=0;
    }
    else {
      direction[i]=(dif_angles[i]>0) ? 1 :-1;
      
    }
  }
/*  Serial.println("start t1");
  //속력 증가 구간
  for(int d_1=0,delay_t1=200; d_1<duration ;d_1++){
    
    for (int j=0;j<4;j++) {
      //도달 특정 목표각에 도달한다면 
        if (current_angles[j]==dest_angles[j]){
          direction[j]=0;
        }
        current_angles[j]+=direction[j];
    }
    motor1.write(current_angles[0]);
    motor2.write(current_angles[1]);
    motor3.write(current_angles[2]);
    motor4.write(current_angles[3]);
    Serial.println("1");
    delay(delay_t1);
    if (delay_t1<100) {
      continue;
    }
    delay_t1-=40;
  }*/
  //구간 2의 경우 max 값에 의해 결정
//  duration=max/3;
  duration=max;
  //속력 일정 구간
  //Serial.println("start t2");
  for(int d_2 =0;d_2<duration;d_2++){
    //cnt의 경우 모든 direction이 0이 되었을 때(즉 모터가 더 이상 움직이지 않을 때) 종료조건
    for (int j=0,cnt=0;j<4;j++) {
        if (current_angles[j]==dest_angles[j]){
          cnt++;
          direction[j]=0;
          if(cnt==4){
          //  Serial.println("terminate 2");
            return;
          }
        }
        current_angles[j]+=direction[j];
    }
    motor1.write(current_angles[0]);
    motor2.write(current_angles[1]);
    motor3.write(current_angles[2]);
    motor4.write(current_angles[3]);
   // Serial.println("2");
    delay(40);
  }

  //속력 감소 구간, 해당 구간은 모두 목표각으로 갔을 때가 종료시점
 /* Serial.println("start t3");
  while(1) {
    int delay_t3=40;
    for (int j=0,cnt=0;j<4;j++) {
        if (current_angles[j]==dest_angles[j]){
          cnt++;
          direction[j]=0;
          if (cnt==4) {
            Serial.println("terminate 3");
          
            return; 
            }
        }
        current_angles[j]+=direction[j];
    }
    motor1.write(current_angles[0]);
    motor2.write(current_angles[1]);
    motor3.write(current_angles[2]);
    motor4.write(current_angles[3]);
    Serial.println("3");
    delay(delay_t3);
    
    if (delay_t3>300) {
      continue;
    }
    delay_t3+=50;
  }*/
  
}
