import numpy as np
from midiutil import MIDIFile
import os
from midi2audio import FluidSynth
from music21 import converter, instrument, note, chord
from tempfile import NamedTemporaryFile
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import json
import shutil


def create_midi_file(melody, file_name):
    track = 0
    channel = 0
    time = 0
    duration = 1  # quarter note
    tempo = 120
    volume = 100

    note_mapping = {
        "1": 60,  # C
        "2": 62,  # D
        "3": 64,  # E
        "4": 65,  # F
        "5": 67,  # G
    }

    midifile = MIDIFile(1, adjust_origin=False)
    midifile.addTempo(track, time, tempo)
    midifile.addTimeSignature(track, time, 5, 4, 24)

    for i, note in enumerate(melody):
        midifile.addNote(track, channel, note_mapping[note], i * duration, duration, volume)

    with open(file_name, "wb") as output_file:
        midifile.writeFile(output_file)

melody_array = np.array([0])

for i in [1, 2, 3, 4, 5]:
    for j in [1, 2, 3, 4, 5]:
        for k in [1, 2, 3, 4, 5]:
            for l in [1, 2, 3, 4, 5]:
                for m in [1, 2, 3, 4, 5]:
                    x = i * 10000 + j * 1000 + k * 100 + l * 10 + m * 1
                    melody_array = np.append(melody_array, x)

str_arr = [str(num) for num in melody_array[1:]]
char_arr = [list(num_str) for num_str in str_arr]

for melody in char_arr:
    file_name = f"midi_{''.join(melody)}.mid"
    create_midi_file(melody, file_name)

def schmulevich_complexity(midi_file):
    midi = converter.parse(midi_file)
    notes_to_parse = midi.flat.notes

    note_transitions = {}

    for i in range(len(notes_to_parse) - 1):
        note1 = notes_to_parse[i]
        note2 = notes_to_parse[i + 1]

        if isinstance(note1, note.Note):
            note1 = note1.pitch
        elif isinstance(note1, chord.Chord):
            note1 = '.'.join(str(n) for n in note1.pitches)

        if isinstance(note2, note.Note):
            note2 = note2.pitch
        elif isinstance(note2, chord.Chord):
            note2 = '.'.join(str(n) for n in note2.pitches)

        transition = (note1, note2)
        if transition in note_transitions:
            note_transitions[transition] += 1
        else:
            note_transitions[transition] = 1

    complexity = 0
    total_transitions = sum(note_transitions.values())
    for count in note_transitions.values():
        probability = count / total_transitions
        complexity -= probability * np.log2(probability)

    return complexity

complexity_dict = {}

for melody, midi_name in zip(char_arr, str_arr):
    midi_file_name = f"midi_{midi_name}.mid"
    complexity = schmulevich_complexity(midi_file_name)
    complexity_dict[midi_name] = complexity

# Create an output directory for the images
output_dir = Path("images")
output_dir.mkdir(exist_ok=True)

result_dict = {}

for melody, midi_name in zip(char_arr, str_arr):
    img_file_name = f"image_{midi_name}.png"
    img_path = output_dir / img_file_name

    # Set up keys for note names and positions
    note_map = {
        "1": "C",
        "2": "D",
        "3": "E",
        "4": "F",
        "5": "G"
    }

    note_position = {
        "1": 0,
        "2": 0.1,
        "3": 0.2,
        "4": 0.3,
        "5": 0.4
    }

   # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(6, 3))

    # Define the height and width of the ellipses
    height = 0.2
    width = 0.15

    # Define the colors for each note
    colors = {'C': 'red', 'D': 'yellow', 'E': 'green', 'F': 'blue', 'G': 'purple'}

    # Set up the staff lines
    line_height = height
    staff_lines = [-0.2,0, 0.2, 0.4, 0.6]
    ax.plot([-1, 1], [staff_lines, staff_lines], color='black', zorder=1)

    # Calculate the spacing between the ellipses along the x-axis
    x_spacing = 0.45

    # Calculate the initial x-coordinate for the first ellipse
    x_start = -x_spacing * (len(melody) - 1) / 2

    # Plot each note as an ellipse on the staff
    for i, note in enumerate(melody):
        note_name = note_map[note]
        x = x_start + i * x_spacing
        y = note_position[note]
        color = colors[note_name]
        ellipse = Ellipse((x, y), width, height, angle=-45, facecolor=color, edgecolor='black', linewidth=1.5, zorder=2)
        ax.add_patch(ellipse)

    # Set the limits of the x and y axes and remove the axis ticks
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.3, 0.7)
    ax.set_xticks([])
    ax.set_yticks([])

    # Remove bounding box
    for spine in ax.spines.values():
        spine.set_visible(False)
        
 
    # Save the figure as a PNG file with an ASCII filename
    with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, bbox_inches='tight')
        tmpfile.flush()

        # Copy the temporary file to the desired location with the correct filename
        shutil.copy(tmpfile.name, img_path)

    plt.close(fig)

    result_dict[midi_name] = {'image': str(img_path), 'complexity': complexity_dict[midi_name]}

print(result_dict)

# Sort the dictionary by complexity
sorted_result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]['complexity']))

# Save the dictionary as a JSON file
with open("melodies_data.json", "w") as json_file:
    json.dump(sorted_result_dict, json_file, indent=4)