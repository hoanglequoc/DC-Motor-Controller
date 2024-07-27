#include <Arduino.h>

int OutPin_Current = A3;
const int voltageSensorPin = A2;          // sensor pin

const float vCC = 5.00;                   // Arduino input voltage (measurable by voltmeter)
const float cur_offset = 0.06;
const float vol_multiplier = 4.97;

int counter = 0;
float test_vol=0.0;
float test_cur=0.0;

void setup ()
{
  Serial.begin(9600);
}

void loop()
{
  unsigned int x=0;
  float total_cur=0.0, total_vol=0.0000;

  for (int x = 0; x < 1000; x++)
  {
    // Current
    total_cur = total_cur + (.049 * analogRead(A3) -25);
  }

  for (int x = 0; x < 1000; x++)
  {
    // Voltage 
    total_vol = total_vol + analogRead(voltageSensorPin);
  } 
            
  test_cur = test_cur + -(total_cur/1000.0 + cur_offset);
  
  test_vol = test_vol + (total_vol/1000.0000/1023.0000) * vCC;

  counter++;
  
  if (counter == 10){
    // Current
    Serial.print(-test_cur/counter,7);
    Serial.print(",");
    Serial.print(test_vol*vol_multiplier/counter,7);
    
    Serial.print("\n");

    test_vol = 0;
    test_cur = 0;
    counter = 0;
  }
  
  delay(1);
}