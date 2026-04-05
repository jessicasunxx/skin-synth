"""WebSocket server that reads serial from the ESP32 and broadcasts JSON messages
to connected browser clients. Run with the project venv.
"""
import asyncio
import json
import serial
import websockets

SERIAL_PORT = "/dev/cu.usbserial-58EB0142621"
BAUD_RATE = 115200

clients = set()

async def serial_reader(queue):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print("Could not open serial port:", e)
        return
    print("Serial opened", SERIAL_PORT)
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            await asyncio.sleep(0.01)
            continue
        parts = line.split(',')
        if len(parts) == 6:
            mode = int(parts[0])
            pads = [int(x) for x in parts[1:]]
            msg = json.dumps({"mode": mode, "pads": pads})
            await queue.put(msg)

async def broadcaster(queue):
    while True:
        msg = await queue.get()
        if clients:
            await asyncio.wait([ws.send(msg) for ws in clients])

async def handler(ws, path):
    clients.add(ws)
    try:
        async for _ in ws:  # ignore incoming
            pass
    finally:
        clients.remove(ws)

async def main():
    queue = asyncio.Queue()
    server = await websockets.serve(handler, '0.0.0.0', 8765)
    print('WebSocket server listening on ws://0.0.0.0:8765')
    await asyncio.gather(serial_reader(queue), broadcaster(queue))

if __name__ == '__main__':
    asyncio.run(main())
