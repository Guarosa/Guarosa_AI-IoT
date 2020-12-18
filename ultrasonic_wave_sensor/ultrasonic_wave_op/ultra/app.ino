#include <SoftwareSerial.h>
#include <PubSubClient.h>

int echoPin = 4;
int triggerPin = 5;
int ledpin = 9;

void setup() {
    Serial.begin(9600);
    pinMode(echoPin, INPUT);
    pinMode(triggerPin, OUTPUT);
    pinMode(ledpin, OUTPUT);
    digitalWrite(ledpin, false);
    digitalWrite(ledpin, LOW); 

    Serial.begin(9600);
    pinMode(echoPin, INPUT);
    pinMode(triggerPin, OUTPUT);
    pinMode(ledpin, OUTPUT);
    digitalWrite(ledpin, false);
    // pinMode(ledpin, OUTPUT);
    digitalWrite(ledpin, LOW);
}

void loop() {
    // trigger 핀으로 10us의 펄스를 발생
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);
    // echo 핀 입력으로부터 거리를 cm 단위로 계산
    int distance = pulseIn(echoPin, HIGH) / 58;
    Serial.println("Distance(cm) = " + String(distance));
    delay(1000);

    // 거리값이 45cm 이하
    if (distance < 45){
        digitalWrite(ledpin, HIGH); // LED제어
    }
    else
    {
        digitalWrite(ledpin, LOW); // LED제어
    }
    
}