import os
import json

# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/layer_cleanup.log'

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
                
                modified = False
                # Check each layer for keys other than "male" or "female"
                for layer_key, layer_value in data.items():
                    if layer_key.startswith('layer_'):
                        keys_to_delete = [key for key in layer_value.keys() if key not in ['male', 'female']]
                        for key in keys_to_delete:
                            del layer_value[key]
                            modified = True
                
                # Save the modified JSON file back to disk if it was modified
                if modified:
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                    log_file.write(f'Modified file: {filename}\n')
            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')