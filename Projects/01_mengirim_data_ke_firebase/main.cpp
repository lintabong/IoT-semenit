#include <Arduino.h>
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>
#include <WiFiUdp.h>

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID "Default"
#define WIFI_PASSWORD "default234"
#define API_KEY ""
#define DATABASE_URL ""
#define BASE_LOCATION "test"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

bool signupOK = false;

void setup() {
    Serial.begin(115200);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    config.api_key = API_KEY;
    config.database_url = DATABASE_URL;

    if (Firebase.signUp(&config, &auth, "", "")) {
      Serial.println("ok");
      signupOK = true;
    }
    else {
      Serial.printf("%s\n", config.signer.signupError.message.c_str());
    }

    config.token_status_callback = tokenStatusCallback;

    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);

    randomSeed(analogRead(A0));
}

void loop() {
    int randomValue = analogRead(A0);

    if (Firebase.RTDB.setInt(&fbdo, (String(BASE_LOCATION) + "/random"), randomValue)) {
        Serial.printf("Berhasil mengirim data: %d\n", randomValue);
    } else {
        Serial.printf("Gagal Mengirim data: %s\n", fbdo.errorReason().c_str());
    }

    delay(1000);
}