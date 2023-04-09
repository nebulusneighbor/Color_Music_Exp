import mido
import keyboard

# Map MIDI note numbers to ASCII key codes
note_to_key = {
    36: '1',  # C2
    38: '2',  # D2
    40: '3',  # E2
    41: '4',  # F2
    43: '5',  # G2
    48: '1',  # C3
    50: '2',  # D3
    52: '3',  # E3
    53: '4',  # F3
    55: '5',  # G3
    60: '1',  # C4
    62: '2',  # D4
    64: '3',  # E4
    65: '4',  # F4
    67: '5',  # G4
    72: '1',  # C5
    74: '2',  # D5
    76: '3',  # E5
    77: '4',  # F5
    79: '5',  # G5
}

def on_message(msg):
    if msg.type == 'note_on' and msg.velocity > 0:
        key = note_to_key.get(msg.note)
        if key:
            keyboard.press(key)
            keyboard.release(key)

# Get the input MIDI port
input_port = mido.open_input()

print("Listening for MIDI input. Press Ctrl+C to exit.")
try:
    for msg in input_port:
        on_message(msg)
except KeyboardInterrupt:
    pass

# Close the input MIDI port
input_port.close()
print("Closed MIDI input.")
