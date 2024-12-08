import os
import json
import openai
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define the folder path containing the JSON files
folder_path = 'sheettest'
log_file_path = 'logs/update_variants_with_gpt.log'

# Ensure the directory for the log file exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_file_path),
    logging.StreamHandler()
])

# Set your OpenAI API key
openai.api_key = ''

def generate_variant_details(name, variant_name, file_path):
    prompt = f"Generate the full name, description, and element for an item with the name '{name}' and variant '{variant_name}' from the file '{file_path}'. The description should add some LORE to the item, considering the LORE is dead soldiers (like in Shaman King). The element should follow the name and description and be one of: NORMAL, FEU, EAU, ELECTRIC, PLANTE, GLACE, COMBAT, POISON, ROCHE, LUMIERE, TENEBRE, ACIER."
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Open the log file in write mode
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
                for variant in data['variants']:
                    if isinstance(variant, dict) and 'name' in variant:
                        # Generate details using ChatGPT
                        details = generate_variant_details(data['name'], variant['name'], file_path)
                        details_lines = details.split('\n')
                        if len(details_lines) >= 3:
                            variant['full_name'] = details_lines[0].replace('Full name: ', '')
                            variant['description'] = details_lines[1].replace('Description: ', '')
                            variant['element'] = details_lines[2].replace('Element: ', '')
                            modified = True
                        else:
                            logging.error(f'{filename}: Failed to generate details for variant {variant["name"]}')
            
            # Save the modified JSON file back to disk if it was modified
            if modified:
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                logging.info(f'{Fore.GREEN}Modified file: {filename}')
            else:
                logging.info(f'{Fore.YELLOW}No modifications needed for file: {filename}')
        except Exception as e:
            logging.error(f'{Fore.RED}{filename}: Error - {str(e)}')