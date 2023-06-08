import random
import json
from psychopy import visual, core, event, monitors, gui
import csv
import time
import os
from psychopy.clock import Clock


# GUI to enter participant details
myDlg = gui.Dlg(title="Participant Details")
myDlg.addText('Enter Participant Details:')
myDlg.addField('ID:')
myDlg.addField('Condition Number:')
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel

if myDlg.OK:  # then the user pressed OK
    print(ok_data)
else:
    print('user cancelled')

participant_id = ok_data[0]
condition_number = ok_data[1]

# Choose the correct JSON file based on the condition number
json_file_name = "melodies_data_color.json" if condition_number in ['2', '4'] else "melodies_data_bw.json"

# Load the dictionary from the chosen JSON file
with open(json_file_name, "r") as json_file:
    melodies_data = json.load(json_file)

# Depending on the condition, choose image directory
image_directory = "images_bw" if condition_number in ['1', '3'] else "images_color"
print(f'Using image directory: {image_directory}')  # debugging output


# Create the prompts dictionary using the data from the JSON file
prompts = {}
for key, value in melodies_data.items():
    prompts[key] = {
        'image': os.path.join(image_directory, str(value['image'])),  # Add the correct directory to image path
        'complexity': value['complexity']
    }

# Define complexity range
max_complexity = max(value['complexity'] for value in melodies_data.values())
complexity_increment = max_complexity / 10


def get_prompt_by_complexity_level(level, prompts, complexity_increment, available_prompts):
    min_complexity = complexity_increment * (level - 1)
    max_complexity = complexity_increment * level

    if level == 10:  # If the current level is the maximum
        filtered_prompts = [
            key for key, value in available_prompts.items()
            if min_complexity <= value['complexity'] <= max_complexity
        ]
    else:
        filtered_prompts = [
            key for key, value in available_prompts.items()
            if min_complexity <= value['complexity'] < max_complexity
        ]

    if not filtered_prompts:
        return None, level == 10

    selected_prompt = random.choice(filtered_prompts)

    # Remove the chosen prompt from available_prompts
    available_prompts.pop(selected_prompt)

    return selected_prompt, level == 10


def get_correct_key_presses(target, response):
    return sum([1 for t, r in zip(target, response) if t == r])

def warmup(win, warmup_directory):
    """Warmup routine that shows all images in a directory."""
    json_file_name = 'warmup_data_bw.json' if warmup_directory == 'images_wu_bw' else 'warmup_data_color.json'
    with open(json_file_name, "r") as json_file:
        warmup_data = json.load(json_file)

    # The initial task message
    task_msg = 'Press\n' + \
               '\nSPACE\n' + \
               '\nWhen you are ready'
    msg_stim = visual.TextStim(win, text=task_msg, pos=(0, 0), color='black')

    for key, value in warmup_data.items():
        # Show the initial task message
        msg_stim.draw()
        win.flip()
        # Wait for SPACE to start warmup trial
        event.waitKeys(keyList=['space'])

        image_stim = visual.ImageStim(win, image=os.path.join(warmup_directory, value['image']), size=(2.0, 2.0), pos=(0, 0.1))  # Adjust position here
        image_stim.draw()
        win.flip()

        # Wait for sequence of 7 key presses to proceed
        response = []
        while len(response) < 7:  # waiting for exactly 7 keypresses to proceed
            keys = event.getKeys(keyList=['1', '2', '3', '4', '5','6','7','space', 'escape'])
            for key in keys:
                # Check if the key is "escape", if so, exit the experiment
                if key[0] == 'escape':
                    core.quit()

                response.append(key[0])

        # clear the window
        win.flip()
        core.wait(1.0)

    # Show a final message at the end of the warmup
    msg_stim.setText("Congratulations, you're finished with warmup!")
    msg_stim.draw()
    win.flip()

    # Keep the final message on the screen for 2 seconds
    core.wait(2.0)



def main():
    # Start setting up the experiment
    mon = monitors.Monitor('MSI', width=53.0, distance=70.0)
    win = visual.Window(fullscr=True, monitor=mon, color="white", size=[0,0])


    task_msg = 'Press\n' + \
               '\nSPACE\n' + \
               '\nWhen you are ready'

    msg_stim = visual.TextStim(win, text=task_msg, pos=(0, 0), color='black')

    complexity_range = 1
    exit_experiment = False

    # Depending on the condition, choose warmup image directory
    warmup_directory = "images_wu_bw" if condition_number in ['1', '3'] else "images_wu_color"
    print(f'Using warmup image directory: {warmup_directory}')  # debugging output

    # Run warmup no timing
    warmup(win, warmup_directory)

    # Start experiment and time
    start_time = time.time()

    available_prompts = prompts.copy()
    complexity_range = 1

    # Create results array
    results = []

    # Start complexity level
    complexity_level = 1
    new_complexity_level = 1  # Initialize new_complexity_level here

    # Counter for total prompts
    total_prompts = 0

    while total_prompts < 110:

        prompt, max_complexity_reached = None, False
        escape_pressed = False

        while not prompt:
            prompt, max_complexity_reached = get_prompt_by_complexity_level(complexity_level, prompts, complexity_increment, available_prompts)
            if not prompt:
                complexity_level += 1
                complexity_level = min(complexity_level, 10)
                if complexity_level == 10:
                    break

        if not prompt:
            print("No available prompts at complexity level", complexity_level)
            break

        msg_stim.draw()
        win.flip()

        rest_time_start = time.time()
        keys = event.waitKeys(keyList=['space'])
        rest_time_end = time.time()

        complexity_level = new_complexity_level
        num_trials = 0
        num_correct_trials = 0

        msg_stim.setText(task_msg)

        if 'space' in keys:
            image = visual.ImageStim(win, image=prompts[prompt]['image'], size=(2.0, 2.0), pos=(0, 0.3))
            image.draw()
            win.flip()

            response = []
            key_timestamps = []
            trial_clock = Clock()

            while len(response) < len(prompt):
                keys = event.getKeys(keyList=['1', '2', '3', '4', '5','6','7','escape'], timeStamped=trial_clock)

                for key in keys:
                    if key[0] == 'escape':
                        exit_experiment = True
                        escape_pressed = True
                        break

                    response.append(key[0])
                    key_timestamps.append(key[1])

                core.wait(0.01)

            if escape_pressed:
                break

            rest_time = rest_time_end - rest_time_start

            win.flip()
            core.wait(1.0)

            msg_stim.setText(task_msg)

        if escape_pressed:
            break

        if exit_experiment:
            break

        if 'escape' in response:
            break

        correct_keys = get_correct_key_presses(prompt, response)
        num_trials += 1
        if correct_keys == len(prompt):
            num_correct_trials += 1

        if num_trials >= 1:
            accuracy = num_correct_trials / num_trials
            if accuracy >= 0.8:
                new_complexity_level = min(complexity_level + 1, 10)
            else:
                new_complexity_level = max(1, complexity_level - 1)

            num_trials = 0
            num_correct_trials = 0

        total_prompts += 1

        end_time = time.time()
        total_time_taken = end_time - start_time

        result = {
            'participant_id': participant_id,
            'condition_number': condition_number,
            'prompt': prompt,
            'response': ''.join(response),
            'correct_keys': correct_keys,
            'complexity_level': complexity_level,
            'rest_time': rest_time,
            'key_timestamps': key_timestamps,
            'prompt_time': trial_clock.getTime(),  # update to get the last prompt time
            'total_time_taken': total_time_taken
        }
        results.append(result)

        complexity_level = new_complexity_level

    end_time = time.time()
    total_time_taken = end_time - start_time

    # Write the results to a CSV file
    with open(os.path.join('results', f'results_{participant_id}.csv'), 'w', newline='') as csvfile:
        fieldnames = ['participant_id', 'condition_number', 'prompt', 'response', 'correct_keys', 'complexity_level', 'rest_time', 'key_timestamps', 'keystamp_1', 'keystamp_2', 'keystamp_3', 'keystamp_4', 'keystamp_5', 'keystamp_6', 'keystamp_7', 'prompt_time', 'total_time_taken']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:

            #keystamp times
            for i, timestamp in enumerate(result['key_timestamps'], start=1):
                result[f'keystamp_{i}'] = timestamp

            #write the rest of the info
            writer.writerow(result)

    win.close()
    core.quit()

    return total_time_taken

if __name__ == "__main__":
    main()
