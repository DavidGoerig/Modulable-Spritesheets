import os
import json
from collections import defaultdict

# Define the folder path containing the JSON files
# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/filecolor.log'

# Ensure the directory for the log file exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Initialize a dictionary to count occurrences of each variant
variant_counts = defaultdict(int)

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
                        for variant in data['variants']:
                            variant_counts[variant] += 1
                        total_variants_count += len(data['variants'])
                        log_file.write(f'{filename}: {len(data["variants"])} variants\n')
                    else:
                        log_file.write(f'{filename}: "variants" key does not exist\n')
            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')

    # Log the total number of variants
    log_file.write(f'Total number of variants: {total_variants_count}\n')

    # Sort the variants by their counts
    sorted_variant_counts = sorted(variant_counts.items(), key=lambda item: item[1], reverse=True)

    # Log the total number of each variant
    log_file.write('\nTotal counts for each variant:\n')
    for variant, count in sorted_variant_counts:
        log_file.write(f'{variant}: {count}\n')