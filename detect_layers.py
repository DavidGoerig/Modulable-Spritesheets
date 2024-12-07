import os
import json

# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/layer_check.log'

# Ensure the directory for the log file exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

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
                    
                    # Check each layer for keys other than "male" or "female"
                    for layer_key, layer_value in data.items():
                        if layer_key.startswith('layer_'):
                            has_other_keys = False
                            has_male_or_female = False
                            for key in layer_value.keys():
                                if key in ['male', 'female']:
                                    has_male_or_female = True
                                else:
                                    has_other_keys = True
                            if has_other_keys and not has_male_or_female:
                                log_file.write(f'File: {filename}, Path: {file_path}, Key: {key}, Value: {layer_value[key]}\n')
            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')