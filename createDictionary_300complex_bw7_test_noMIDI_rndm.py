import numpy as np
from collections import defaultdict
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile
import random

def calculate_complexity_from_sequence(sequence):
    note_transitions = defaultdict(int)

    for i in range(len(sequence) - 1):
        transition = (sequence[i], sequence[i + 1])
        note_transitions[transition] += 1

    complexity = 0
    total_transitions = sum(note_transitions.values())
    for count in note_transitions.values():
        probability = count / total_transitions
        complexity -= probability * np.log2(probability)

    return complexity


def generate_melody_image(melody, img_path):
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

    fig, ax = plt.subplots(figsize=(25, 12.5))
    ax.set_aspect('equal')

    height = 0.125
    width = 0.08

    color = 'black'

    line_height = height
    staff_lines = [-0.3, -0.1875, -0.075, 0.0375, 0.15, 0.2625]
    ax.plot([-1, 1], [staff_lines, staff_lines], color='black', zorder=1)

    x_spacing = 0.3
    x_start = -x_spacing * (len(melody) - 1) / 2

    for i, note in enumerate(melody):
        note_name = note_map[note]
        x = x_start + i * x_spacing
        y = note_position[note]
        ellipse = Ellipse((x, y), width, height, angle=-45, facecolor=color, edgecolor='black', linewidth=1.5, zorder=2)
        ax.add_patch(ellipse)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.3, 0.7)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, bbox_inches='tight')
        tmpfile.flush()

        shutil.copy(tmpfile.name, img_path)

    plt.close(fig)


melody_array = np.array([0])

for i in range(1, 8):
    for j in range(1, 8):
        for k in range(1, 8):
            for l in range(1, 8):
                for m in range(1, 8):
                    for n in range(1, 8):
                        for o in range(1, 8):
                            x = i * 1000000 + j * 100000 + k * 10000 + l * 1000 + m * 100 + n * 10 + o
                            melody_array = np.append(melody_array, x)

str_arr = [str(num) for num in melody_array[1:]]
char_arr = [list(num_str) for num_str in str_arr]

result_dict = {}
complexity_dict = {}

print('Calculating complexities...')
for melody in char_arr:
    complexity = calculate_complexity_from_sequence(melody)
    complexity_dict[''.join(melody)] = complexity

complexity_items = list(complexity_dict.items())
complexity_items.sort(key=lambda item: item[1])

num_groups = 10
group_size = len(complexity_items) // num_groups
complexity_groups = [complexity_items[i:i+group_size] for i in range(0, len(complexity_items), group_size)]

if len(complexity_groups) < num_groups:
    complexity_groups[-1].extend(complexity_items[num_groups*group_size:])

complexity_groups = complexity_groups[:num_groups]

group_counters = defaultdict(int)

output_dir = Path("images")
output_dir.mkdir(exist_ok=True)

print('Generating melody images...')
for group_index, group in enumerate(complexity_groups):
    random_group = random.sample(group, min(300, len(group)))  # Select 300 melodies at random
    for melody_name, complexity in random_group:
        img_path = output_dir / f"{melody_name}.png"
        print(f"Generating image for melody: {melody_name}")

        generate_melody_image(list(melody_name), img_path)

        result_dict[melody_name] = {'image': str(img_path), 'complexity': complexity}

        group_counters[group_index] += 1

sorted_result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]['complexity']))

with open("melodies_data.json", "w") as json_file:
    json.dump(sorted_result_dict, json_file, indent=4)

print('Image generation completed.')
