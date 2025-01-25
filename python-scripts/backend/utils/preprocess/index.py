import json
import re

# Load the dataset
with open("data.json", "r") as f:
    data = json.load(f)

def standardize_prompt(prompt):
    """
    Standardize the input prompt by normalizing spacing and casing.
    
    Args:
        prompt (str): Raw natural language description of the scene.
        
    Returns:
        str: Normalized prompt.
    """
    prompt = prompt.lower().strip()
    prompt = re.sub(r"\s+", " ", prompt)  # Remove extra spaces
    return prompt

def standardize_tscn_format(tscn_file):
    """
    Normalize the formatting of a .tscn file for consistency.
    
    Args:
        tscn_file (str): Path to the .tscn file.
        
    Returns:
        str: Normalized .tscn content as a string.
    """
    with open(tscn_file, "r") as f:
        lines = f.readlines()
    
    normalized_lines = []
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Skip empty lines
            normalized_lines.append(line)
    
    return "\n".join(normalized_lines)

# Preprocess the data
processed_data = []
for entry in data:
    # Normalize the prompt
    prompt = standardize_prompt(entry["prompt"])
    
    # Normalize the .tscn output
    tscn_output = standardize_tscn_format(entry["output"])
    
    processed_data.append({"prompt": prompt, "output": tscn_output})

# Save the processed data for future use
with open("processed_data.json", "w") as f:
    json.dump(processed_data, f, indent=4)

print("Preprocessing complete. Data saved to processed_data.json.")
