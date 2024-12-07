import os
import json

# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/variantperjson.log'

# Ensure the directory for the log file exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Initialize a counter for the total number of variants
total_variants_count = 0

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
                    
                    # Check if the "variants" key exists and count the variants
                    if 'variants' in data:
                        variants_count = len(data['variants'])
                        total_variants_count += variants_count
                        log_file.write(f'{filename}: {variants_count} variants\n')
                    else:
                        log_file.write(f'{filename}: "variants" key does not exist\n')
            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')

    # Log the total number of variants
    log_file.write(f'Total number of variants: {total_variants_count}\n')