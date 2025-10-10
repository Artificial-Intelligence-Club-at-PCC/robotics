#include <Servo.h>

#define NUM_LEGS 6
#define SERVOS_PER_LEG 3
#define TOTAL_SERVOS (NUM_LEGS * SERVOS_PER_LEG)

Servo servos[TOTAL_SERVOS];

// Only the first servo (index 0) is actually connected for now
int servoPins[TOTAL_SERVOS] = {
  2, 3, 4,    // Leg 1
  5, 6, 7,    // Leg 2
  8, 9, 10,   // Leg 3
  11, 12, 13, // Leg 4
  14, 15, 16, // Leg 5
  17, 18, 19  // Leg 6
};

// Walking parameters
int walkSpeed = 50;  // 0–100
int legLift = 20;    // 0–50
unsigned long moveInterval = 800;

void setup() {
  Serial.begin(9600);
  Serial.println("🕷️ Hexapod Ready - Awaiting Commands from Python");

  // Attach all servo objects (only pin 2 physically connected now)
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    if (i == 0) {
      servos[i].attach(servoPins[i]);
      Serial.print("Servo["); Serial.print(i); Serial.println("] attached to D2 (ACTIVE)");
    } else {
      Serial.print("Servo["); Serial.print(i); Serial.println("] simulated (not attached)");
    }
  }

  // Neutral position
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    writeServo(i, 90);
  }
  delay(1000);
  Serial.println("Neutral position set.");
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    switch (cmd) {
      case 'F': moveForward(); break;
      case 'B': moveBackward(); break;
      case 'L': turnLeft(); break;
      case 'R': turnRight(); break;
      case 'S': {
        int val = Serial.parseInt();
        walkSpeed = constrain(val, 0, 100);
        moveInterval = map(walkSpeed, 0, 100, 1200, 300);
        Serial.print("Speed set to: "); Serial.println(walkSpeed);
        break;
      }
      case 'H': {
        int val = Serial.parseInt();
        legLift = constrain(val, 0, 50);
        Serial.print("Leg height set to: "); Serial.println(legLift);
        break;
      }
    }
  }
}

// ---------------- MOVEMENT FUNCTIONS ----------------

void moveForward() {
  Serial.println("🕷️ Moving Forward...");
  simulateAllLegs();
  moveServo(0, 0);  // active servo demonstration
}

void moveBackward() {
  Serial.println("🕷️ Moving Backward...");
  simulateAllLegs();
  moveServo(0, 180);
}

void turnLeft() {
  Serial.println("↩️ Turning Left...");
  simulateAllLegs();
  moveServo(0, 45);
}

void turnRight() {
  Serial.println("↪️ Turning Right...");
  simulateAllLegs();
  moveServo(0, 135);
}

// --------------- SIMULATION / DEMO FUNCTIONS ----------------

void simulateAllLegs() {
  Serial.print("Simulating "); Serial.print(TOTAL_SERVOS - 1);
  Serial.println(" servos (only D2 active)");
}

void moveServo(int index, int angle) {
  writeServo(index, angle);
  delay(400);
  writeServo(index, 90);  // return to center
}

void writeServo(int index, int angle) {
  if (index == 0) {  // Only servo 0 is physically attached
    servos[index].write(angle);
  }
  // For simulated servos, we just print feedback
  Serial.print("Servo["); Serial.print(index);
  Serial.print("] -> "); Serial.print(angle);
  Serial.println("°");
}
