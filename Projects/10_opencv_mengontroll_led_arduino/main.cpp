#include <Arduino.h>


const int ledPin = 9;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int ledIndex = input.charAt(0) - '0';
    int brightness = input.substring(2).toInt();
    
    switch (ledIndex) {
      case 0: analogWrite(ledPin, brightness); break;
    }
  }
}