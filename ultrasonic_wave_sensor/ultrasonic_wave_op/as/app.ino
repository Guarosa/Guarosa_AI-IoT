#include <SoftwareSerial.h>
#include <WiFiEsp.h>
#include <PubSubClient.h>
#include <SimpleTimer.h>
#include <WifiUtil.h>

//SoftwareSerial softSerial(2, 3);           // RX, TX
const char ssid[] = "Campus7_Room3_2.4";               // 네트워크 SSID
const char password[] = "12345678";       // 비밀번호
const char mqtt_server[] = "192.168.0.121"; // 서버 주소

// MQTT용 WiFi 클라이언트 객체 초기화
WifiUtil wifi(2, 3);
WiFiEspClient espClient;
PubSubClient client(espClient);

int echoPin = 4;
int triggerPin = 5;
int relaypin = 6;
int relaypin2 = 9;

void callback(char *topic, byte*payload, unsigned int length) {
    payload[length] = NULL;
    char *message = payload;

    if (strcmp("1", message) == 0) { // 여기 가습기 작동
        digitalWrite(relaypin,HIGH);     // 1채널 릴레이 ON
        digitalWrite(relaypin2,HIGH);
        delay(1000);
        digitalWrite(relaypin2,LOW);
        delay(10000);
        digitalWrite(relaypin,LOW);      // 1채널 릴레이 OFF
    }
    Serial.print(topic);
    Serial.print(" : ");
    Serial.println(message);
}

void mqtt_init() {
    client.setServer(mqtt_server, 1883);
    // subscriber인경우 메시지 수신시 호출할 콜백 함수 등록
    client.setCallback(callback);
}

// MQTT 서버에 접속될 때까지 재접속 시도
void reconnect() {

    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        
        if (client.connect("ESP8266Client")) {
            Serial.println("connected");
            // subscriber로 등록
            client.subscribe("iot/home/#",1);  // 구독 신청
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void publish() {
    char message[10];
    // int readVal = analogRead(pSensor);
    // dtostrf(readVal, 5, 2, message);
    // 토픽 발행
    // client.publish("iot/home/Illuminance", message);

}

// 2초 간격으로 publish
SimpleTimer timer;


void setup() {
    Serial.begin(9600);
    pinMode(echoPin, INPUT);
    pinMode(triggerPin, OUTPUT);
    pinMode(13, OUTPUT);
    digitalWrite(13, false);
    wifi.init(ssid, password);
    mqtt_init();
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    pinMode(relaypin,OUTPUT); 
}

void loop() {
    // trigger 핀으로 10us의 펄스를 발생
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);
    // echo 핀 입력으로부터 거리를 cm 단위로 계산
    int distance = pulseIn(echoPin, HIGH) / 58;
    // Serial.println("Distance(cm) = " + String(distance));
    delay(1000);

    // 거리값이 10cm 이하
    if (distance < 10){
        digitalWrite(13, HIGH); // LED제어
    }
    else
    {
        digitalWrite(13, LOW); // LED제어
    }

    if (!client.connected()) {  // MQTT가 연결 X
        reconnect();
    }
    client.loop();
    timer.run();
    
}