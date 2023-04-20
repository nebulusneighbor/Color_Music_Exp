import random
import json
from psychopy import visual, core, event
import csv

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
    # Create a window
    
    
    win = visual.Window(color='white', fullscr=True) # OG (800,600), fullscr=False
    # Define the task message prompt
    task_msg = 'Press\n' + \
               '\nSPACE\n' + \
               '\nWhen you are ready'


    # Create a text stimulus for the message prompt
    msg_stim = visual.TextStim(win, text=task_msg, pos=(0, 0), color='black')


    complexity_range = 1
    num_trials = 0
    num_correct_trials = 0
    exit_experiment = False
    
    # Initialize the list to store the results
    results = []

    while True:
        prompt = get_prompt_by_complexity_range(complexity_range, complexity_range + 1, prompts)
        if not prompt:
            break
            
        # Draw the message prompt on the window
        msg_stim.draw()
        win.flip()
        
        # Wait for the participant to press the spacebar
        keys = event.waitKeys(keyList=['space'])

        # If spacebar was pressed, show a blank screen for 3 seconds
        if 'space' in keys:
            
            # Display the image associated with the prompt
            image = visual.ImageStim(win, image=prompts[prompt]['image'])
            image.draw()
            win.flip()

            response = []
            while len(response) < len(prompt):
                key = event.waitKeys(keyList=['1', '2', '3', '4', '5', 'escape'])
                if key[0] == 'escape':
                    exit_experiment = True
                    break
                response.extend(key)
                
            win.flip()
            core.wait(3.0)
                
        
        if exit_experiment:
            break

        if 'escape' in response:
            break

        # Check the number of correct key presses considering the order
        correct_keys = get_correct_key_presses(prompt, response)
        num_trials += 1
        if correct_keys == len(prompt):
            num_correct_trials += 1

        # Update the complexity range based on the adaptive staircase method
        if num_trials >= 5:
            accuracy = num_correct_trials / num_trials
            if accuracy >= 0.8:
                complexity_range += 1
            else:
                complexity_range = max(1, complexity_range - 1)
            # Reset the trials count and correct trials count
            num_trials = 0
            num_correct_trials = 0
         # Save the result of this trial
       
        result = {
            'prompt': prompt,
            'response': ''.join(response),
            'correct_keys': correct_keys,
            'complexity_range': complexity_range
        }
        results.append(result)

        

    # Write the results to a CSV file
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['prompt', 'response', 'correct_keys', 'complexity_range']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)


    win.close()
    core.quit()

if __name__ == "__main__":
    main()
