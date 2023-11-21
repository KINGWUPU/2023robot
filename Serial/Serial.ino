//simple serial tset
//,로 구분된 4가지 정수를 받아들여 값이 배열에 정확히 저장되는지 확인해보는 파일
int current_angles[4]={60,60,60,60};
int dest_angles[4]={60,60,60,60};
//현재각과 목표각의 차이 저장
int dif_angles[4]={0,0,0,0};
void setup() {
  // put your setup code here, to run once:
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
    for (int j=0;j<4;j++) {
      dif_angles[j]=dest_angles[j]-current_angles[j];
      current_angles[j]=dest_angles[j];
    }
    Serial.println("Your dest :");
    for (int i=0 ;i<4;i++ ){
      Serial.println(dest_angles[i]);
    }
    Serial.println("difference :");
    for (int k=0 ;k<4;k++ ){
      Serial.println(dif_angles[k]);
    }
    Serial.println("Done");
  }
  
}
