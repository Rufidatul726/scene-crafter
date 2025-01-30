import requests
import json

def process_prompt(prompt):
    # Check if the prompt asks for script creation
    if "script" in prompt.lower():
        # Prepare the payload to request the GDScript creation from the API
        payload = {
            "instruction": f"Create a GDScript for a node named '{node_name}' with the following prompt: ",
            "script": f"{prompt}_script.gd",  # Assuming script name is based on the node
            "prompt": prompt 
        }

        # Call the API to get the generated GDScript
        response = requests.post("http://localhost:8001/recommend/", json=payload)

        if response.status_code == 200:
            gdscript_code = response.json().get('script', '')

            # Verify the suggestions in the response
            response = response.json().get('response', [])
            response = extract_script(response)
            
            return response
        else:
            print(f"Failed to generate script. API Error: {response.status_code}")
            return null
    else:
        print(f"No action required from the prompt: {prompt}")
        return null


def extract_script(gdscript_code):
    """
    Extracts the relevant script content from the provided GDScript.
    This removes everything before and after the actual script content starting with "extends".
    """

    # Find where the script starts with "extends"
    start_idx = gdscript_code.lower().find("extends")
    
    if start_idx != -1:
        # Extract the content from the "extends" keyword onwards
        script_content = gdscript_code[start_idx:]
        return script_content.strip()
    else:
        print("No 'extends' found in the script. Invalid script structure.")
        return ""