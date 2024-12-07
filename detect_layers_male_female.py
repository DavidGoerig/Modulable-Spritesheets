import os
import json

# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/layer_gender_count.log'

# Ensure the directory for the log file exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Initialize counters
male_count = 0
female_count = 0
both_count = 0
none_count = 0

# Open the log file in write mode
with open(log_file_path, 'w') as log_file:
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Open and load the JSON file
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    
                    # Check each layer for "male" and "female" keys
                    has_male = False
                    has_female = False
                    for layer_key, layer_value in data.items():
                        if layer_key.startswith('layer_'):
                            if 'male' in layer_value:
                                has_male = True
                            if 'female' in layer_value:
                                has_female = True
                    
                    # Update counters based on presence of "male" and "female"
                    if has_male and has_female:
                        both_count += 1
                    elif has_male:
                        male_count += 1
                    elif has_female:
                        female_count += 1
                    else:
                        none_count += 1

            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')

    # Log the counts
    log_file.write(f'Total files with both male and female: {both_count}\n')
    log_file.write(f'Total files with only male: {male_count}\n')
    log_file.write(f'Total files with only female: {female_count}\n')
    log_file.write(f'Total files with neither male nor female: {none_count}\n')