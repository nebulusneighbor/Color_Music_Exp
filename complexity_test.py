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

#Define complexity range
max_complexity = max(value['complexity'] for value in melodies_data.values())
complexity_increment = max_complexity / 15

def get_prompt_by_complexity_level(level, prompts, complexity_increment):
    min_complexity = complexity_increment * (level - 1)
    max_complexity = complexity_increment * level
    print(min_complexity)##DEBUG
    print(max_complexity)##DEBUG

    if level == 15:  # If the current level is the maximum
        filtered_prompts = [
            key for key, value in prompts.items()
            if min_complexity <= value['complexity'] <= max_complexity  # Notice the "<=" instead of "<"
        ]
    else:
        filtered_prompts = [
            key for key, value in prompts.items()
            if min_complexity <= value['complexity'] < max_complexity
        ]

    if filtered_prompts:
        return random.choice(filtered_prompts), level == 15
    else:
        return None, level == 15

    # filtered_prompts = [
    #     key for key, value in prompts.items()
    #     if min_complexity <= value['complexity'] < max_complexity
    # ]

    # if filtered_prompts:
    #     return random.choice(filtered_prompts), level == 15
    # else:
    #     return None, level == 15

# #DEBUG
# print(max_complexity)
# print(complexity_increment)

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
    exit_experiment = False

    #create results array
    results = []

    #Start coimplexity level
    complexity_level = 1
    new_complexity_level = 1  # Initialize new_complexity_level here

    # Counter for max complexity encounters
    max_complexity_counter = 0

    while True:
        prompt, max_complexity_reached = None, False
        while not prompt:  # Keep increasing complexity level until a prompt is found or max complexity is reached
            prompt, max_complexity_reached = get_prompt_by_complexity_level(complexity_level, prompts, complexity_increment)
            if not prompt:
                complexity_level += 1
                # Add upperbound to increase
                complexity_level = min(complexity_level, 15)
                print(complexity_level)##DEBUG
                if complexity_level == 15:  # Break the inner loop if max complexity is reached
                    break

        if not prompt:  # If no prompt was found, it means max complexity was reached and there were no available prompts
            print("No available prompts at complexity level", complexity_level) # Print a message indicating that there are no available prompts at this complexity level
            break  # Break the outer loop and end the experiment

        # If the complexity_level has reached the max, increment max_complexity_counter
        if max_complexity_reached:
            max_complexity_counter += 1
            print(max_complexity_counter)##DEBUG
            if max_complexity_counter >= 15:  # Exits the program when the participant encounters 15 samples at max complexity
                break


        msg_stim.draw()
        win.flip()

        rest_time_start = time.time()
        keys = event.waitKeys(keyList=['space'])
        rest_time_end = time.time()

        complexity_level=new_complexity_level
        num_trials = 0
        num_correct_trials = 0

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

        if num_trials >= 1: ### DEBUG: 1, other 5
            accuracy = num_correct_trials / num_trials
            if accuracy >= 0.8:
                #complexity_level += 1
                new_complexity_level = min(complexity_level + 1,15)
                print(new_complexity_level)##DEBUG
            else:
                new_complexity_level = max(1, complexity_level - 1)

            num_trials = 0
            num_correct_trials = 0

        end_time = time.time()
        total_time_taken = end_time - start_time


        result = {
            'prompt': prompt,
            'response': ''.join(response),
            'correct_keys': correct_keys,
            'complexity_level': new_complexity_level,
            'rest_time': rest_time,
            'time_to_start': time_to_start,
            'key_timestamps': key_timestamps,
            'total_time_taken': total_time_taken
        }
        results.append(result)

        complexity_level = new_complexity_level  # Update complexity level at the end of successful iteration

    end_time = time.time()
    total_time_taken = end_time - start_time

    # Write the results to a CSV file
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['prompt', 'response', 'correct_keys', 'complexity_level', 'rest_time', 'time_to_start', 'key_timestamps','total_time_taken']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    win.close()
    core.quit()

    return total_time_taken


if __name__ == "__main__":
    main()