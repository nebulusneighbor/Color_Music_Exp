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

# Create the output directory
os.makedirs('images', exist_ok=True)

def generate_image(melody):
    note_map = {
        "1": "C",
        "2": "D",
        "3": "E",
        "4": "F",
        "5": "G",
        "6": "A",
        "7": "B"
    }

    note_position = {
        "1": -0.1875,
        "2": -0.13125,
        "3": -0.075,
        "4": -0.01875,
        "5": 0.0375,
        "6": 0.09375,
        "7": 0.15
    }

    colors = {
        "C": "red",
        "D": "orange",
        "E": "yellow",
        "F": "green",
        "G": "blue",
        "A": "purple",
        "B": "magenta"
    }

    fig, ax = plt.subplots(figsize=(25, 12.5))
    ax.set_aspect('equal')

    height = 0.125
    width = 0.08
    line_height = height
    staff_lines = [-0.3, -0.1875, -0.075, 0.0375, 0.15, 0.2625]
    ax.plot([-1, 1], [staff_lines, staff_lines], color='black', zorder=1)
    x_spacing = 0.3
    x_start = -x_spacing * (len(melody) - 1) / 2

    for i, note in enumerate(melody):
        note_name = note_map[note]
        color = colors[note_name]
        x = x_start + i * x_spacing
        y = note_position[note]
        ellipse = Ellipse((x, y), width, height, angle=-45, facecolor=color, edgecolor='black', linewidth=1.5, zorder=2)
        ax.add_patch(ellipse)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.4, 0.4)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("images/melody_" + ''.join(melody) + ".png", bbox_inches='tight')
    plt.close(fig)

generate_image(['1', '2', '3', '4', '5', '6', '7'])
generate_image(['7','6','5','4','3','2','1'])
generate_image(['1','1','1','1','1','2','1'])
generate_image(['2','2','2','2','3','2','1'])
generate_image(['3','3','4','5','4','3','3'])
generate_image(['3','2','1','1','3','5','3'])
generate_image(['1','2','3','1','2','3','4'])
generate_image(['7','6','5','6','5','4','3'])
generate_image(['7','6','5','4','3','2','1'])
generate_image(['1','3','5','7','5','3','1'])
generate_image(['2','4','6','7','6','4','2'])
