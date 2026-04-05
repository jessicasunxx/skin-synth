# Skin Synth

Two-part project: an ESP32 touch instrument that sends pad states over serial, and a laptop Python program that visualizes the touches.

Layout

- `skin-synth/esp32-touch-instrument/` — PlatformIO project for ESP32
  - `platformio.ini` — project config
  - `src/main.cpp` — touch instrument sketch (prints `mode,p1,p2,p3,p4,p5`)
  - `src/calibrate.cpp` — helper sketch to read raw touch values for calibration
- `skin-synth/laptop-visuals/` — desktop visuals
  - `main.py` — reads serial and draws visuals with `pygame`
  - `requirements.txt` — `pyserial` and `pygame`

Quick start

1. ESP32 (PlatformIO)

   - Open VS Code PlatformIO and open the folder `skin-synth/esp32-touch-instrument`.
   - If you have a TTGO T-Display, you may prefer using the existing root `platformio.ini` board `ttgo-t1` instead of `esp32dev`.
   - Build, Upload, then Monitor (115200). You should see comma-separated lines like `1,0,1,0,0,0`.
   - If touch detection is flaky, flash `src/calibrate.cpp` and watch raw values to pick a good threshold.

2. Laptop

   - Open `skin-synth/laptop-visuals`.
   - Install dependencies:

```bash
pip install -r requirements.txt
```

   - Edit `main.py` and set `SERIAL_PORT` to your device (mac: `ls /dev/tty.*`).
   - Run:

```bash
python main.py
```

Next ideas

- Add ambient/rhythm mode visuals and sound (synth) on laptop.
- Send richer data (pressure / raw values) from ESP32 for more expressive visuals.
