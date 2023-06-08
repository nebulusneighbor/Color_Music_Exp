import rtmidi
import keyboard
import time

# Map MIDI note numbers to ASCII key codes
note_to_key = {
    36: '1',  # C2
    38: '2',  # D2
    40: '3',  # E2
    41: '4',  # F2
    43: '5',  # G2
    45: '6',  # A2
    47: '7',  # B2
    48: '1',  # C3
    50: '2',  # D3
    52: '3',  # E3
    53: '4',  # F3
    55: '5',  # G3
    57: '6',  # A3
    59: '7',  # B3
    60: '1',  # C4
    62: '2',  # D4
    64: '3',  # E4
    65: '4',  # F4
    67: '5',  # G4
    69: '6',  # A4
    71: '7',  # B4
    72: '1',  # C5
    74: '2',  # D5
    76: '3',  # E5
    77: '4',  # F5
    79: '5',  # G5
    81: '6',  # A5
    83: '7',  # B5
}

def on_message(msg):
    if msg[0] == 144 and msg[2] > 0:  # note_on event
        print("Received MIDI note:", msg[1])  # Print the received MIDI note
        key = note_to_key.get(msg[1])
        if key:
            print("Mapped to key:", key)  # Print the mapped key
            keyboard.press_and_release(key)
            time.sleep(0.1)

midi_in = rtmidi.MidiIn()
ports = midi_in.get_ports()

if not ports:
    print("No MIDI input ports available. Exiting.")
    exit(1)

print("Available MIDI input ports:")
for i, port in enumerate(ports):
    print(f"[{i}] {port}")

port_idx = int(input("Select the MIDI input port index: "))

midi_in.open_port(port_idx)

print("Listening for MIDI input. Press Ctrl+C to exit.")
try:
    while True:
        msg = midi_in.get_message()
        if msg:
            on_message(msg[0])
        time.sleep(0.001)
except KeyboardInterrupt:
    pass

midi_in.close_port()
print("Closed MIDI input.")
