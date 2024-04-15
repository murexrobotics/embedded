/// MIT License
///
/// Copyright (c) 2024 Altan Ünver and Byran Huang
///
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
///
/// The above copyright notice and this permission notice shall be included in all
/// copies or substantial portions of the Software.
///
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
/// SOFTWARE.


// ------------- Enter Field and Target Time Here --------------
enum Move { Forward, Backward, Left, Right, Start, End };


const int time_offset = 0;
Move path[16] = {Start, Forward, Right, Left, Forward, Backward, End};
const int path_len = 7;


// ------------- DO NOT MODIFY BELOW --------------
#include <Arduino.h>

// Motor Pins
// M1 - LEFT, M2 - RIGHT
#define M1_IN1 3
#define M1_IN2 2
#define M2_IN1 1
#define M2_IN2 0
#define M1_ENCODER_A 14
#define M1_ENCODER_B 15
#define M2_ENCODER_A 17
#define M2_ENCODER_B 16

int target1 = 0;
int pos1 = 0;
bool wheel1done = false;
void readEncoder1() {
    // Serial.print("Running enc1");
    int b = digitalRead(M1_ENCODER_B);
    wheel1done = false;
    if (target1 >= 0 && (b==0)) {
        Serial.println("Target Reached");
        digitalWrite(M1_IN1, LOW);
        analogWrite(M1_IN2, 0);
        wheel1done = true;
    }
    else if (target1 <= 0 && !(b==0)) {
        Serial.println("Target Reached");
        digitalWrite(M1_IN2, LOW);
        analogWrite(M1_IN1, 0);
        wheel1done = true;
    }
    if (b > 0) {
        pos1++;
        target1--;
    }
    else {
        pos1--;
        target1++;
    };
}

int target2 = 0;
int pos2 = 0;
bool wheel2done = false;
void readEncoder2() {
    // Serial.print("Running enc2");
    int b = digitalRead(M2_ENCODER_B);
    wheel2done = false;
    if (target2 <= 0 && b == 0) {
        Serial.println("Target Reached");
        digitalWrite(M2_IN1, LOW);
        analogWrite(M2_IN2, 0);
        wheel2done = true;
    }
    else if (target2 >= 0 && !(b==0)) {
        Serial.println("Target Reached");
        digitalWrite(M2_IN2, LOW);
        analogWrite(M2_IN1, 0);
        wheel2done = true;
    }
    if (b > 0) {
        pos2++;
        target2++;
    }
    else {
        pos2--;
        target2--;
    };
}
// motor functions

int turnConstant = 26;

bool turn_right() {
    pos2 = 0;
    pos1 = 0;
    target1 = -turnConstant * 16.5517;
    target2 = turnConstant * 16.5517;
    digitalWrite(M1_IN2, LOW);
    digitalWrite(M2_IN2, LOW);
    analogWrite(M1_IN1, 55);
    analogWrite(M2_IN1, 55);
    delay(70);
    analogWrite(M1_IN1, 105);
    analogWrite(M2_IN1, 105);
    delay(70);
    analogWrite(M1_IN1, 155);
    analogWrite(M2_IN1, 155);
    delay(70);
    analogWrite(M1_IN1, 205);
    analogWrite(M2_IN1, 205);
    delay(70);
    analogWrite(M1_IN1, 255);
    analogWrite(M2_IN1, 255);
    return true;
}

bool turn_left() {
    pos2 = 0;
    pos1 = 0;
    target1 = turnConstant * 16.5517;
    target2 = -turnConstant * 16.5517;
    digitalWrite(M1_IN1, LOW);
    digitalWrite(M2_IN1, LOW);
    analogWrite(M1_IN2, 55);
    analogWrite(M2_IN2, 55);
    delay(70);
    analogWrite(M1_IN2, 105);
    analogWrite(M2_IN2, 105);
    delay(70);
    analogWrite(M1_IN2, 155);
    analogWrite(M2_IN2, 155);
    delay(70);
    analogWrite(M1_IN2, 205);
    analogWrite(M2_IN2, 205);
    delay(70);
    analogWrite(M1_IN2, 255);
    analogWrite(M2_IN2, 255);
    return true;
}

bool forwards(int distance) {
    pos2 = 0;
    pos1 = 0;
    target1 = distance * 16.5517;
    target2 = distance * 16.5517;
    digitalWrite(M1_IN1, LOW);
    digitalWrite(M2_IN2, LOW);
    analogWrite(M1_IN2, 55);
    analogWrite(M2_IN1, 55);
    delay(200);
    analogWrite(M1_IN2, 105);
    analogWrite(M2_IN1, 105);
    delay(200);
    analogWrite(M1_IN2, 155);
    analogWrite(M2_IN1, 155);
    delay(200);
    analogWrite(M1_IN2, 205);
    analogWrite(M2_IN1, 205);
    delay(200);
    analogWrite(M1_IN2, 255);
    analogWrite(M2_IN1, 255);
    return true;
}

bool backwards(int distance) {
    pos2 = 0;
    pos1 = 0;
    target1 = -distance * 16.5517;
    target2 = -distance * 16.5517;
    digitalWrite(M1_IN2, LOW);
    digitalWrite(M2_IN1, LOW);
    analogWrite(M2_IN2, 55);
    analogWrite(M1_IN1, 55);
    delay(200);
    analogWrite(M2_IN2, 105);
    analogWrite(M1_IN1, 105);
    delay(200);
    analogWrite(M2_IN2, 155);
    analogWrite(M1_IN1, 155);
    delay(200);
    analogWrite(M2_IN2, 205);
    analogWrite(M1_IN1, 205);
    delay(200);
    analogWrite(M2_IN2, 255);
    analogWrite(M1_IN1, 255);
    return true;
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    pinMode(M1_IN1, OUTPUT);
    pinMode(M1_IN2, OUTPUT);
    pinMode(M1_ENCODER_A, INPUT);
    pinMode(M1_ENCODER_B, INPUT);
    pinMode(M2_IN1, OUTPUT);
    pinMode(M2_IN2, OUTPUT);
    pinMode(M2_ENCODER_A, INPUT);
    pinMode(M2_ENCODER_B, INPUT);

    attachInterrupt(digitalPinToInterrupt(M1_ENCODER_A), readEncoder1, RISING);
    attachInterrupt(digitalPinToInterrupt(M2_ENCODER_A), readEncoder2, RISING);

    pinMode(25, OUTPUT);
    digitalWrite(25, HIGH);
    delay(100);
    digitalWrite(25, LOW);
}

bool hasRun = false;
int path_index = 0;

void loop() {
    Serial.print("->Path Index: ");
    Serial.println(path_index);
    Serial.print(millis());
    Serial.print("    Wheel 1 Pos:");
    Serial.print(pos1);
    Serial.print("      Wheel 1 Target:");
    Serial.print(target1);
    Serial.print("    ->    Wheel 2 Pos:");
    Serial.print(pos2);
    Serial.print("      Wheel 2 Target:");
    Serial.println(target2);
    Serial.print("       Wheel 1 Done: ");
    Serial.println(wheel1done);
    Serial.print("      Wheel 2 Done: ");
    Serial.println(wheel2done);
    delay(50);

    if (wheel1done && wheel2done) {
        delay(900);
        path_index++;
        hasRun = false;
    }

    if (path_index >= path_len) {
        return;
    }

    if (time_offset != 0) {
        delay((time_offset * 1000)/path_len);
    }

    if (!hasRun)
    if (path[path_index] == Forward) {
        hasRun = forwards(50);
    } else if (path[path_index] == Backward) {
        hasRun = backwards(50);
    } else if (path[path_index] == Right) {
        hasRun = turn_right();
    } else if (path[path_index] == Left) {
        hasRun = turn_left();
    }
}