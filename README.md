# Skin Synth

An ESP32 touch instrument that sends pad states over serial, paired with desktop and browser visualizers that turn touches into shapes and sound.

## How It Works

The ESP32 reads five capacitive touch pads and prints CSV over serial (`mode,p1,p2,p3,p4,p5`). Pad 5 toggles between two modes. A host program—either a Python/pygame desktop app or a WebSocket-backed browser page—reads the stream, draws reactive visuals, and plays tones mapped to each pad.

**Mode 1** — soft sine tones, dark blue background  
**Mode 2** — punchy square-wave tones, dark red background

## Project Structure

```
skin-synth/
├── esp32-touch-instrument/   ESP32 firmware (PlatformIO / Arduino)
│   ├── platformio.ini
│   └── src/main.cpp
├── laptop-visuals/           Desktop visualizer (Python + pygame)
│   ├── main.py
│   └── requirements.txt
└── web-visuals/              Browser visualizer (WebSocket + Canvas)
    ├── server.py
    ├── index.html
    └── requirements.txt
```

## Getting Started

### Prerequisites

- [PlatformIO](https://platformio.org/) (VS Code extension or CLI)
- Python 3.8+
- An ESP32 board with exposed touch pins

### 1. Flash the ESP32

```bash
cd esp32-touch-instrument
pio run -e esp32dev -t upload
pio device monitor -b 115200
```

You should see lines like `1,0,1,0,0,0`. If detection is flaky, adjust the `threshold` constant in `src/main.cpp`.

> **TTGO T-Display users:** use the `ttgo-t1` PlatformIO environment instead of `esp32dev`.

### 2a. Run the Desktop Visualizer

```bash
cd laptop-visuals
pip install -r requirements.txt
```

Edit `SERIAL_PORT` in `main.py` to match your device (on macOS run `ls /dev/tty.*` to find it), then:

```bash
python main.py
```

### 2b. Run the Web Visualizer

```bash
cd web-visuals
pip install -r requirements.txt
```

Edit `SERIAL_PORT` in `server.py`, then start the WebSocket server:

```bash
python server.py
```

Open `index.html` in a browser (or serve it locally). The page connects to `ws://<hostname>:8765` automatically.

## Pin Mapping

| Pad | GPIO | Touch Channel | Role         |
|-----|------|---------------|--------------|
| 1   | 2    | T2            | Note A3      |
| 2   | 12   | T5            | Note C4      |
| 3   | 33   | T8            | Note D4      |
| 4   | 32   | T9            | Note E4      |
| 5   | 27   | T7            | Mode toggle  |

## Ideas

- Ambient / rhythm mode with generative visuals
- Send raw pressure values from ESP32 for more expressive response
- MIDI output over BLE
