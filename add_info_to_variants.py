import os
import json

# Define the folder path containing the JSON files
folder_path = 'sheet_definitions'
log_file_path = 'logs/update_variants.log'

# Define the default details for each variant
default_variant_details = {
    "name": "",
    "full_name": "",
    "description": "",
    "icon_path": "",
    "spell": 1,
    "rare": 1,
    "element": 1
}

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
                # Check if the "variants" key exists and update the structure
                if 'variants' in data:
                    updated_variants = []
                    for variant in data['variants']:
                        if isinstance(variant, str):
                            # Convert string variant to object with default details
                            variant_obj = {"name": variant}
                            variant_obj.update(default_variant_details)
                            updated_variants.append(variant_obj)
                            modified = True
                        elif isinstance(variant, dict) and 'name' in variant:
                            # Ensure the variant has all the default details
                            for key, value in default_variant_details.items():
                                if key not in variant:
                                    variant[key] = value
                                    modified = True
                            updated_variants.append(variant)
                        else:
                            log_file.write(f'{filename}: Invalid variant format\n')
                    data['variants'] = updated_variants
                
                # Save the modified JSON file back to disk if it was modified
                if modified:
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                    log_file.write(f'Modified file: {filename}\n')
                else:
                    log_file.write(f'No changes needed for file: {filename}\n')
            except json.JSONDecodeError:
                log_file.write(f'{filename}: Failed to decode JSON\n')
            except Exception as e:
                log_file.write(f'{filename}: Error - {str(e)}\n')