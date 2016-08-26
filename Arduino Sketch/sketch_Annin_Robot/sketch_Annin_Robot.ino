/* Annin Robot - Stepper motor robot control software
    Copyright (C) 2016  Chris Annin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    chris.annin@gmail.com
*/    

#include <Servo.h>

Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;

String inData;
String function;

const int J1stepPin = 2;
const int J1dirPin = 3;
const int J2stepPin = 4;
const int J2dirPin = 5;
const int J3stepPin = 6;
const int J3dirPin = 7;
const int J4stepPin = 8;
const int J4dirPin = 9;
const int J5stepPin = 10;
const int J5dirPin = 11;
const int J6stepPin = 12;
const int J6dirPin = 13;

const int Input22 = 22;
const int Input23 = 23;
const int Input24 = 24;
const int Input25 = 25;
const int Input26 = 26;
const int Input27 = 27;
const int Input28 = 28;
const int Input29 = 29;
const int Input30 = 30;
const int Input31 = 31;
const int Input32 = 32;
const int Input33 = 33;
const int Input34 = 34;
const int Input35 = 35;
const int Input36 = 36;
const int Input37 = 37;

const int Output38 = 38;
const int Output39 = 39;
const int Output40 = 40;
const int Output41 = 41;
const int Output42 = 42;
const int Output43 = 43;
const int Output44 = 44;
const int Output45 = 45;
const int Output46 = 46;
const int Output47 = 47;
const int Output48 = 48;
const int Output49 = 49;
const int Output50 = 50;
const int Output51 = 51;
const int Output52 = 52;
const int Output53 = 53;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);
  pinMode(A6, OUTPUT);
  pinMode(A7, OUTPUT);

  pinMode(J1stepPin, OUTPUT);
  pinMode(J1dirPin, OUTPUT);
  pinMode(J2stepPin, OUTPUT);
  pinMode(J2dirPin, OUTPUT);
  pinMode(J3stepPin, OUTPUT);
  pinMode(J3dirPin, OUTPUT);
  pinMode(J4stepPin, OUTPUT);
  pinMode(J4dirPin, OUTPUT);
  pinMode(J5stepPin, OUTPUT);
  pinMode(J5dirPin, OUTPUT);
  pinMode(J6stepPin, OUTPUT);
  pinMode(J6dirPin, OUTPUT);

  pinMode(Input22, INPUT);
  pinMode(Input23, INPUT);
  pinMode(Input24, INPUT);
  pinMode(Input25, INPUT);
  pinMode(Input26, INPUT);
  pinMode(Input27, INPUT);
  pinMode(Input28, INPUT);
  pinMode(Input29, INPUT);
  pinMode(Input30, INPUT);
  pinMode(Input31, INPUT);
  pinMode(Input32, INPUT);
  pinMode(Input33, INPUT);
  pinMode(Input34, INPUT);
  pinMode(Input35, INPUT);
  pinMode(Input36, INPUT);
  pinMode(Input37, INPUT);

  pinMode(Output38, OUTPUT);
  pinMode(Output39, OUTPUT);
  pinMode(Output40, OUTPUT);
  pinMode(Output41, OUTPUT);
  pinMode(Output42, OUTPUT);
  pinMode(Output43, OUTPUT);
  pinMode(Output44, OUTPUT);
  pinMode(Output45, OUTPUT);
  pinMode(Output46, OUTPUT);
  pinMode(Output47, OUTPUT);
  pinMode(Output48, OUTPUT);
  pinMode(Output49, OUTPUT);
  pinMode(Output50, OUTPUT);
  pinMode(Output51, OUTPUT);
  pinMode(Output52, OUTPUT);
  pinMode(Output53, OUTPUT);

  servo0.attach(A0);
  servo1.attach(A1);
  servo2.attach(A2);
  servo3.attach(A3);
  servo4.attach(A4);
  servo5.attach(A5);
  servo6.attach(A6);
  servo7.attach(A7);

  digitalWrite(Output38, HIGH);
  digitalWrite(Output39, HIGH);
  digitalWrite(Output40, HIGH);
  digitalWrite(Output41, HIGH);
  digitalWrite(Output42, HIGH);
  digitalWrite(Output43, HIGH);
  digitalWrite(Output44, HIGH);
  digitalWrite(Output45, HIGH);

}


void loop() {
  while (Serial.available() > 0)
  {
    char recieved = Serial.read();
    inData += recieved;
    // Process message when new line character is recieved
    if (recieved == '\n')
    {
      String function = inData.substring(0, 2);


      //-----COMMAND TO MOVE SERVO---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "SV")
      {
        int SVstart = inData.indexOf('V');
        int POSstart = inData.indexOf('P');
        int servoNum = inData.substring(SVstart + 1, POSstart).toInt();
        int servoPOS = inData.substring(POSstart + 1).toInt();
        if (servoNum == 0)
        {
          servo0.write(servoPOS);
        }
        if (servoNum == 1)
        {
          servo1.write(servoPOS);
        }
        if (servoNum == 2)
        {
          servo2.write(servoPOS);
        }
        if (servoNum == 3)
        {
          servo3.write(servoPOS);
        }
        if (servoNum == 4)
        {
          servo4.write(servoPOS);
        }
        if (servoNum == 5)
        {
          servo5.write(servoPOS);
        }
        if (servoNum == 6)
        {
          servo6.write(servoPOS);
        }
        if (servoNum == 7)
        {
          servo7.write(servoPOS);
        }
        Serial.print("Servo Done");
      }




      //-----COMMAND TO WAIT TIME---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "WT")
      {
        int WTstart = inData.indexOf('S');
        float WaitTime = inData.substring(WTstart + 1).toFloat();
        int WaitTimeMS = WaitTime * 1000;
        delay(WaitTimeMS);
        Serial.print("Done");
      }

      //-----COMMAND IF INPUT THEN JUMP---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "IJ")
      {
        int IJstart = inData.indexOf('X');
        int IJTabstart = inData.indexOf('T');
        int IJInputNum = inData.substring(IJstart + 1, IJTabstart).toInt();
        if (digitalRead(IJInputNum) == HIGH)
        {
          Serial.println("True\n");
        }
        if (digitalRead(IJInputNum) == LOW)
        {
          Serial.println("False\n");
        }
      }
      //-----COMMAND SET OUTPUT ON---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "ON")
      {
        int ONstart = inData.indexOf('X');
        int outputNum = inData.substring(ONstart + 1).toInt();
        digitalWrite(outputNum, HIGH);
        Serial.print("Done");
      }
      //-----COMMAND SET OUTPUT OFF---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "OF")
      {
        int ONstart = inData.indexOf('X');
        int outputNum = inData.substring(ONstart + 1).toInt();
        digitalWrite(outputNum, LOW);
        Serial.print("Done");
      }
      //-----COMMAND TO WAIT INPUT ON---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "WI")
      {
        int WIstart = inData.indexOf('N');
        int InputNum = inData.substring(WIstart + 1).toInt();
        while (digitalRead(InputNum) == LOW) {
          delay(100);
        }
        Serial.print("Done");
      }
      //-----COMMAND TO WAIT INPUT OFF---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "WO")
      {
        int WIstart = inData.indexOf('N');
        int InputNum = inData.substring(WIstart + 1).toInt();

        //String InputStr =  String("Input" + InputNum);
        //uint8_t Input = atoi(InputStr.c_str ());
        while (digitalRead(InputNum) == HIGH) {
          delay(100);
        }
        Serial.print("Done");
      }
      //-----COMMAND TO MOVE---------------------------------------------------
      //-----------------------------------------------------------------------
      if (function == "MJ")
      {
        int J1start = inData.indexOf('A');
        int J2start = inData.indexOf('B');
        int J3start = inData.indexOf('C');
        int J4start = inData.indexOf('D');
        int J5start = inData.indexOf('E');
        int J6start = inData.indexOf('F');
        int SPstart = inData.indexOf('S');
        int J1dir = inData.substring(J1start + 1, J1start + 2).toInt();
        int J2dir = inData.substring(J2start + 1, J2start + 2).toInt();
        int J3dir = inData.substring(J3start + 1, J3start + 2).toInt();
        int J4dir = inData.substring(J4start + 1, J4start + 2).toInt();
        int J5dir = inData.substring(J5start + 1, J5start + 2).toInt();
        int J6dir = inData.substring(J6start + 1, J6start + 2).toInt();
        int J1step = inData.substring(J1start + 2, J2start).toInt();
        int J2step = inData.substring(J2start + 2, J3start).toInt();
        int J3step = inData.substring(J3start + 2, J4start).toInt();
        int J4step = inData.substring(J4start + 2, J5start).toInt();
        int J5step = inData.substring(J5start + 2, J6start).toInt();
        int J6step = inData.substring(J6start + 2, SPstart).toInt();
        float SpeedIn = inData.substring(SPstart + 1).toFloat();
        SpeedIn = (SpeedIn / 100);
        float CalcSpeed = (1600 / SpeedIn);
        int Speed = int(CalcSpeed);

        //FIND HIGHEST STEP
        int highStep = J1step;
        if (J2step > highStep)
        {
          highStep = J2step;
        }
        if (J3step > highStep)
        {
          highStep = J3step;
        }
        if (J4step > highStep)
        {
          highStep = J4step;
        }
        if (J5step > highStep)
        {
          highStep = J5step;
        }
        if (J6step > highStep)
        {
          highStep = J6step;
        }



        //DETERMINE AXIS SKIP INCREMENT
        int J1skip = (highStep / J1step);
        int J2skip = (highStep / J2step);
        int J3skip = (highStep / J3step);
        int J4skip = (highStep / J4step);
        int J5skip = (highStep / J5step);
        int J6skip = (highStep / J6step);


        //RESET COUNTERS
        int J1done = 0;
        int J2done = 0;
        int J3done = 0;
        int J4done = 0;
        int J5done = 0;
        int J6done = 0;

        //RESET SKIP CURRENT
        int J1skipCur = 0;
        int J2skipCur = 0;
        int J3skipCur = 0;
        int J4skipCur = 0;
        int J5skipCur = 0;
        int J6skipCur = 0;

        //SET DIRECTIONS
        if (J1dir == 1)
        {
          digitalWrite(J1dirPin, HIGH);
        }
        else if (J1dir == 0)
        {
          digitalWrite(J1dirPin, LOW);
        }
        if (J2dir == 1)
        {
          digitalWrite(J2dirPin, HIGH);
        }
        else if (J2dir == 0)
        {
          digitalWrite(J2dirPin, LOW);
        }
        if (J3dir == 1)
        {
          digitalWrite(J3dirPin, HIGH);
        }
        else if (J3dir == 0)
        {
          digitalWrite(J3dirPin, LOW);
        }
        if (J4dir == 1)
        {
          digitalWrite(J4dirPin, HIGH);
        }
        else if (J4dir == 0)
        {
          digitalWrite(J4dirPin, LOW);
        }
        if (J5dir == 1)
        {
          digitalWrite(J5dirPin, HIGH);
        }
        else if (J5dir == 0)
        {
          digitalWrite(J5dirPin, LOW);
        }
        if (J6dir == 1)
        {
          digitalWrite(J6dirPin, HIGH);
        }
        else if (J6dir == 0)
        {
          digitalWrite(J6dirPin, LOW);
        }




        //DRIVE MOTORS
        while (J1done < J1step || J2done < J2step || J3done < J3step || J4done < J4step || J5done < J5step || J6done < J6step)
        {
          if (J1done < J1step && J1skipCur == 0)
          {
            digitalWrite(J1stepPin, HIGH);
          }
          if (J2done < J2step && J2skipCur == 0)
          {
            digitalWrite(J2stepPin, HIGH);
          }
          if (J3done < J3step && J3skipCur == 0)
          {
            digitalWrite(J3stepPin, HIGH);
          }
          if (J4done < J4step && J4skipCur == 0)
          {
            digitalWrite(J4stepPin, HIGH);
          }
          if (J5done < J5step && J5skipCur == 0)
          {
            digitalWrite(J5stepPin, HIGH);
          }
          if (J6done < J6step && J6skipCur == 0)
          {
            digitalWrite(J6stepPin, HIGH);
          }
          //#############DELAY AND SET LOW
          delayMicroseconds(0);
          if (J1done < J1step && J1skipCur == 0)
          {
            digitalWrite(J1stepPin, LOW);
            J1done = ++J1done;
          }
          if (J2done < J2step && J2skipCur == 0)
          {
            digitalWrite(J2stepPin, LOW);
            J2done = ++J2done;
          }
          if (J3done < J3step && J3skipCur == 0)
          {
            digitalWrite(J3stepPin, LOW);
            J3done = ++J3done;
          }
          if (J4done < J4step && J4skipCur == 0)
          {
            digitalWrite(J4stepPin, LOW);
            J4done = ++J4done;
          }
          if (J5done < J5step && J5skipCur == 0)
          {
            digitalWrite(J5stepPin, LOW);
            J5done = ++J5done;;
          }
          if (J6done < J6step && J6skipCur == 0)
          {
            digitalWrite(J6stepPin, LOW);
            J6done = ++J6done;
          }
          //#############DELAY BEFORE RESTARTING LOOP AND SETTING HIGH AGAIN
          delayMicroseconds(Speed);
          //increment skip count
          J1skipCur = ++J1skipCur;
          J2skipCur = ++J2skipCur;
          J3skipCur = ++J3skipCur;
          J4skipCur = ++J4skipCur;
          J5skipCur = ++J5skipCur;
          J6skipCur = ++J6skipCur;
          //if skiped enough times set back to zero
          if (J1skipCur == J1skip)
          {
            J1skipCur = 0;
          }
          if (J2skipCur == J2skip)
          {
            J2skipCur = 0;
          }
          if (J3skipCur == J3skip)
          {
            J3skipCur = 0;
          }
          if (J4skipCur == J4skip)
          {
            J4skipCur = 0;
          }
          if (J5skipCur == J5skip)
          {
            J5skipCur = 0;
          }
          if (J6skipCur == J6skip)
          {
            J6skipCur = 0;
          }
        }
        inData = ""; // Clear recieved buffer
        Serial.print("Move Done");
      }
      else
      {
        inData = ""; // Clear recieved buffer
      }
    }
  }
}





