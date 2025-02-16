#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

int16_t ax, ay, az;
float angleX, angleY;

void setup() {
  Serial.begin(115200);
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin(); 
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  Serial.println("Initializing MPU...");
  mpu.initialize();
  Serial.println("Testing MPU6050 connection...");
  if(mpu.testConnection() ==  false){
    Serial.println("MPU6050 connection failed");
    while(true){
      Serial.println(".");
    }
  }
  else{
    Serial.println("MPU6050 connection successful");
  }
}

void loop() {
    mpu.getAcceleration(&ax, &ay, &az);
    
    angleX = atan2(ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
    angleY = atan2(ay, sqrt(ax * ax + az * az)) * 180.0 / PI;

    String result = String(int(angleX)) + "," + String(int(angleY));
    Serial.println(result);

    delay(50);
}
