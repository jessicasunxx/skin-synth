#include <Arduino.h>

// Using touch-capable pins. User requested GPIO2 for pad1.
const int pad1 = 2;  // GPIO2 (T2)
const int pad2 = 12; // GPIO12 (T5)
const int pad3 = 33; // GPIO33 (T8)
const int pad4 = 32; // GPIO32 (T9) — changed per request (touch-capable)
const int pad5 = 27; // GPIO27 (T7) - mode toggle

int mode = 1;
unsigned long lastModeSwitch = 0;
const int threshold = 50;

void setup() {
    Serial.begin(115200);
    delay(1000);
}

void loop() {
    int raw1 = touchRead(pad1);
    int raw2 = touchRead(pad2);
    int raw3 = touchRead(pad3);
    int raw4 = touchRead(pad4);
    int raw5 = touchRead(pad5);

    int p1 = raw1 < threshold ? 1 : 0;
    int p2 = raw2 < threshold ? 1 : 0;
    int p3 = raw3 < threshold ? 1 : 0;
    int p4 = raw4 < threshold ? 1 : 0;
    int p5 = raw5 < threshold ? 1 : 0;

    if (p5 == 1 && millis() - lastModeSwitch > 1000) {
        mode = (mode == 1) ? 2 : 1;
        lastModeSwitch = millis();
    }

    Serial.print(mode);
    Serial.print(",");
    Serial.print(p1);
    Serial.print(",");
    Serial.print(p2);
    Serial.print(",");
    Serial.print(p3);
    Serial.print(",");
    Serial.print(p4);
    Serial.print(",");
    Serial.println(p5);

    delay(50);
}
