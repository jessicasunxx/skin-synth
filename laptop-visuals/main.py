import serial
import pygame
import numpy as np

SERIAL_PORT = "/dev/cu.usbserial-58EB0142621"
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception:
    ser = None

# Setup audio: use numpy to generate short tones and play via pygame.sndarray
SAMPLE_RATE = 44100
pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Skin Synth Visuals")
clock = pygame.time.Clock()

def make_tone(freq, duration=0.25, volume=0.5, wave='sine'):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    if wave == 'sine':
        wave_data = np.sin(2 * np.pi * freq * t)
    elif wave == 'square':
        wave_data = np.sign(np.sin(2 * np.pi * freq * t))
    else:
        wave_data = np.sin(2 * np.pi * freq * t)
    audio = (wave_data * 32767 * volume).astype(np.int16)
    return pygame.sndarray.make_sound(audio)

# Define frequencies for pads (mode 1 = soft sine, mode 2 = punchy square)
freqs = [220, 261.63, 293.66, 329.63, 392.00]  # A3, C4, D4, E4, G4
sounds_mode1 = [make_tone(f, duration=0.35, volume=0.35, wave='sine') for f in freqs]
sounds_mode2 = [make_tone(f * 1.5, duration=0.18, volume=0.6, wave='square') for f in freqs]

running = True
mode = 1
pads = [0, 0, 0, 0, 0]
prev_pads = [0, 0, 0, 0, 0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        if ser:
            line = ser.readline().decode("utf-8").strip()
            data = line.split(",")

            if len(data) == 6:
                mode = int(data[0])
                pads = [int(x) for x in data[1:]]
    except Exception:
        pass

    # play sound on pad press (rising edge)
    for i in range(5):
        if pads[i] and not prev_pads[i]:
            if mode == 1:
                sounds_mode1[i].play()
            else:
                sounds_mode2[i].play()
    prev_pads = pads.copy()

    # visuals
    if mode == 1:
        screen.fill((15, 15, 30))
    else:
        screen.fill((30, 10, 10))

    # Spread pads across the screen and make visuals larger/clearer
    width, height = screen.get_size()
    pad_positions = [
        (int(width * 0.12), int(height * 0.6)),
        (int(width * 0.32), int(height * 0.5)),
        (int(width * 0.52), int(height * 0.6)),
        (int(width * 0.72), int(height * 0.5)),
        (int(width * 0.88), int(height * 0.25)),
    ]
    pad_radius = int(min(width, height) * 0.08)

    colors = [(255, 120, 120), (120, 255, 120), (120, 120, 255), (255, 255, 120), (255, 255, 255)]
    for i, pos in enumerate(pad_positions):
        if pads[i]:
            if i % 2 == 0:
                pygame.draw.circle(screen, colors[i], pos, pad_radius)
            else:
                rect = pygame.Rect(0, 0, pad_radius * 2, pad_radius * 2)
                rect.center = pos
                pygame.draw.rect(screen, colors[i], rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
if ser:
    ser.close()
