import json
import os
import re

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

def preprocess_data(train_file_dir, data):
    """
    Preprocess the input data by standardizing the prompt and .tscn output.
    
    Args:
        data (list): List of dictionaries containing the prompt and .tscn output.
        
    Returns:
        list: Processed data with standardized prompt and .tscn output.
    """
    processed_data = []
    for entry in data:
        # Normalize the prompt
        prompt = standardize_prompt(entry["prompt"])
        
        # Normalize the .tscn output
        tscn_output = standardize_tscn_format(os.path.join(train_file_dir, entry["output"]))
        
        processed_data.append({"prompt": prompt, "output": tscn_output})
    
    return processed_data

# Preprocess function for structured tokens for training and evaluation
def preprocess_function(entry, tokenizer):
    """
    Custom preprocessing for structured `.tscn` scene files and natural language prompts.

    Args:
        entry: data entry with prompt and expected `.tscn`.

    Returns:
        dict: Tokenized prompt and output with special formatting for structured tokens.
    """
    # Tokenize prompt and the expected scene format
    input_encodings = tokenizer(entry["prompt"], truncation=True, padding="max_length", max_length=512)
    output_encodings = tokenizer(entry["output"], truncation=True, padding="max_length", max_length=512)

    return {
        "input_ids": input_encodings["input_ids"],
        "attention_mask": input_encodings["attention_mask"],
        "labels": output_encodings["input_ids"],
    }
