#include <Arduino.h>

// PWM output pin
int pwm_pin_1 = 9;
int pwm_pin_2 = 10;

// LED pin
int led_pin = LED_BUILTIN;

// Motor state and speed variables
bool motorRunning = false;
bool motorForward = false;
int motorSpeed = 0;

void setup() {
  pinMode(pwm_pin_1, OUTPUT);
  pinMode(pwm_pin_2, OUTPUT);
  pinMode(led_pin, OUTPUT);
  TCCR2B = TCCR2B & B11111000 | B00000001; // prescaler of 1

  // begin serial communication
  Serial.begin(9600);
}

void loop() {
  while (Serial.available() == 0) {}

  char incoming = Serial.read();

  if (incoming >= '0' && incoming <= '9') {
    motorSpeed = map(incoming, '0', '9', 0, 255);
  } else if (incoming == 'F') {
    motorRunning = true;
    motorForward = true;
  } else if (incoming == 'B') {
    motorRunning = true;
    motorForward = false;
  } else if (incoming == 'S') {
    motorRunning = false;
  }

  if (motorRunning) {
    if (motorForward) {
      analogWrite(pwm_pin_1, motorSpeed);
      analogWrite(pwm_pin_2, 0);
      digitalWrite(led_pin, HIGH);
    } else {
      analogWrite(pwm_pin_1, 0);
      analogWrite(pwm_pin_2, motorSpeed);
      blinkLED();
    }
  } else {
    analogWrite(pwm_pin_1, 0);
    analogWrite(pwm_pin_2, 0);
    digitalWrite(led_pin, LOW);
  }
}

void blinkLED() {
  static unsigned long lastBlink = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - lastBlink >= 1000) {
    lastBlink = currentMillis;
    digitalWrite(led_pin, !digitalRead(led_pin));
  }
}