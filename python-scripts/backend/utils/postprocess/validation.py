import re

def check_and_modify_scene_content(scene_content, prompt):
    # Check if '[gd_scene' exists in the scene content
    if not re.search(r'\[gd_scene.*\]', scene_content):
        scene_content = '[gd_scene load_steps=2 format=2]\n' + scene_content

    # Split content into lines
    lines = scene_content.splitlines()

    # Determine if the scene should be 2D or 3D based on the prompt
    is_3d = "3D" in prompt  # If the prompt contains '3D', it is a 3D scene

    # Find the last 'ext_resource' entry and insert a 'node' after it, if no node exists
    last_ext_resource_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('[ext_resource'):
            last_ext_resource_index = i
    
    # Check if there is already a node declaration in the scene
    node_exists = any(line.strip().startswith('[node name=') for line in lines)
    
    if not node_exists:
        # If at least one 'ext_resource' is found, add the 'node' after the last one
        if last_ext_resource_index != -1:
            node_type = "Node3D" if is_3d else "Node2D"  # Choose 3D or 2D node based on the prompt
            lines.insert(last_ext_resource_index + 1, f'[node name="Node2D" type="{node_type}"]')
        else:
            # If no 'ext_resource' found, append 'node' at the end
            node_type = "Node3D" if is_3d else "Node2D"
            lines.append(f'[node name="{node_type}" type="{node_type}"]')

    # Fix any node declarations that are malformed, ensuring proper structure
    for i, line in enumerate(lines):
        if line.strip().startswith('[node name='):
            # Ensure the node declaration ends with a properly closed bracket
            if not line.strip().endswith(']'):
                print(lines[i])
                # Re-format the node line properly if it is missing the closing bracket
                lines[i] = line + "]"

    # Join the lines back into the content
    return '\n'.join(lines)
