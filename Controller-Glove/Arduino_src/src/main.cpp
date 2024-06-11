#include "Wire.h"
#include <Arduino.h>

#define MPU6050_ADDR 0x68 // Alternatively set AD0 to HIGH  --> Address = 0x69
int16_t accX, accY; // Raw register values (accelaration)
char result[7]; // temporary variable used in convert function

int sensorPins[] = {A0, A1, A2, A3}; // array of sensor pins
int sensorValues[4]; // array to hold sensor values

char* toStr(int16_t character) { // converts int16 to string and formatting
  sprintf(result, "%6d", character);
  return result;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // wake up!
  Wire.endTransmission(true);
}

void loop() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. 
                               // As a result, the connection is kept active.
  Wire.requestFrom(MPU6050_ADDR, 4, true); // request a total of 2*2=4 registers
  
  // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same int16_t variable
  accX = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accY = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  
  Serial.print("AcX = "); Serial.print(toStr(accX));
  Serial.print(" | AcY = "); Serial.print(toStr(accY));
  Serial.println();

  for (int i = 0; i < 4; i++) {
    sensorValues[i] = analogRead(sensorPins[i]);
    Serial.print("Sensor ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(sensorValues[i]);
  }

  delay(10);
}