import random
import json
from psychopy import visual, core, event, monitors, gui
import csv
import time


# Load the dictionary from the JSON file
with open("melodies_data.json", "r") as json_file:
    melodies_data = json.load(json_file)

# Create the prompts dictionary using the data from the JSON file
prompts = {}
for key, value in melodies_data.items():
    prompts[key] = {
        'image': str(value['image']),
        'complexity': value['complexity']
    }

def get_prompt_by_complexity_range(min_complexity, max_complexity, prompts):
    filtered_prompts = [
        key for key, value in prompts.items()
        if min_complexity <= value['complexity'] <= max_complexity
    ]
    if filtered_prompts:
        return random.choice(filtered_prompts)
    else:
        return None

def get_correct_key_presses(target, response):
    return sum([1 for t, r in zip(target, response) if t == r])

def main():
    start_time = time.time()
    mon = monitors.Monitor('MSI', width=53.0, distance=70.0)
    win = visual.Window(fullscr=True, monitor=mon, color="white")# winType='pyglet', units='pix', allowStencil=True)
#    win = visual.Window(color='white', fullscr=True)
    task_msg = 'Press\n' + \
               '\nSPACE\n' + \
               '\nWhen you are ready'

    msg_stim = visual.TextStim(win, text=task_msg, pos=(0, 0), color='black')

    complexity_range = 1
    num_trials = 0
    num_correct_trials = 0
    exit_experiment = False

    results = []

    while True:
        prompt = get_prompt_by_complexity_range(complexity_range, complexity_range + 1, prompts)
        if not prompt:
            break

        msg_stim.draw()
        win.flip()

        rest_time_start = time.time()
        keys = event.waitKeys(keyList=['space'])
        rest_time_end = time.time()

        if 'space' in keys:
            time_to_start_start = time.time()

            image = visual.ImageStim(win, image=prompts[prompt]['image'])
            image.draw()
            win.flip()

            response = []
            key_timestamps = []
            while len(response) < len(prompt):
                key = event.waitKeys(keyList=['1', '2', '3', '4', '5', 'escape'], timeStamped=True)
                if key[0][0] == 'escape':
                    exit_experiment = True
                    break
                response.extend(key[0][0])
                key_timestamps.append(key[0][1])

            time_to_start_end = key_timestamps[0] if key_timestamps else time.time()
            time_to_start = time_to_start_end - time_to_start_start
            rest_time = rest_time_end - rest_time_start

            win.flip()
            core.wait(1.0)

        if exit_experiment:
            break

        if 'escape' in response:
            break

        correct_keys = get_correct_key_presses(prompt, response)
        num_trials += 1
        if correct_keys == len(prompt):
            num_correct_trials += 1

        if num_trials >= 5:
            accuracy = num_correct_trials / num_trials
            if accuracy >= 0.8:
                complexity_range += 1
            else:
                complexity_range = max(1, complexity_range - 1)
            num_trials = 0
            num_correct_trials = 0


        result = {
            'prompt': prompt,
            'response': ''.join(response),
            'correct_keys': correct_keys,
            'complexity_range': complexity_range,
            'rest_time': rest_time,
            'time_to_start': time_to_start,
            'key_timestamps': key_timestamps
        }
        results.append(result)

        end_time = time.time()
        total_time_taken = end_time - start_time
        return total_time_taken

        # Write the results to a CSV file
        with open('results.csv', 'w', newline='') as csvfile:
            fieldnames = ['prompt', 'response', 'correct_keys', 'complexity_range', 'rest_time', 'time_to_start', 'key_timestamps']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        win.close()
        core.quit()


if __name__ == "__main__":
    main()
