import re

def remove_duplicate_properties_from_nodes(scene_content):
    """Remove duplicate properties from the same nodes."""
    scene_lines = scene_content.splitlines()
    cleaned_lines = []
    node_properties = {}  # Store node properties as a dictionary

    current_node = None
    node_property_lines = []

    for line in scene_lines:
        # Detect the node line with node name
        if 'node name' in line:
            # If we've reached a new node and it had properties stored, we add them first
            if current_node is not None and node_property_lines:
                # Remove duplicate properties for the current node
                unique_properties = {}
                for prop_line in node_property_lines:
                    match = re.match(r'(\S+) = (.+)', prop_line)
                    if match:
                        key, value = match.groups()
                        if key not in unique_properties:
                            unique_properties[key] = value

                # Rebuild the lines with unique properties for this node
                for key, value in unique_properties.items():
                    cleaned_lines.append(f"{key} = {value}")
            
            # Start a new node
            current_node = line
            node_property_lines = [line]  # Include the node line itself

        # Collect property lines for the current node
        elif current_node and line.strip() != '' and re.match(r'(\S+) = (.+)', line.strip()):
            node_property_lines.append(line)

        else:
            # For all other lines (non-node lines, blank lines), simply append to the result
            if current_node:
                cleaned_lines.append(current_node)
                current_node = None

            cleaned_lines.append(line)
    
    # Handle the last node's properties, if any
    if current_node is not None and node_property_lines:
        unique_properties = {}
        for prop_line in node_property_lines:
            match = re.match(r'(\S+) = (.+)', prop_line)
            if match:
                key, value = match.groups()
                if key not in unique_properties:
                    unique_properties[key] = value

        # Rebuild the lines with unique properties for this node
        for key, value in unique_properties.items():
            cleaned_lines.append(f"{key} = {value}")

    # Reassemble the scene content without duplicate properties for the nodes
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene

def remove_duplicate_lines_from_scene(scene_content):
    """Remove duplicate nodes from the scene content."""
    seen_nodes = set()  # Set to keep track of nodes we've already seen
    scene_lines = scene_content.splitlines()  # Split the scene into individual lines
    cleaned_lines = []

    for line in scene_lines:
        # If a node line, we'll check for its uniqueness
        if "node name" in line:
            node_name_start = line.find('name="') + 6
            node_name_end = line.find('"', node_name_start)
            node_name = line[node_name_start:node_name_end]
            
            # If the node name has been seen before, skip adding this line
            if node_name in seen_nodes:
                continue  # Skip duplicate node
            
            # Add this node name to seen nodes to avoid future duplicates
            seen_nodes.add(node_name)
        
        # Always add the current line (whether it's a duplicate or not)
        cleaned_lines.append(line)

    # Reassemble the scene content without duplicates
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene

def remove_duplicate_ext_resources(scene_content):
    """Remove duplicate ext_resource paths from the scene content."""
    seen_resources = set()  # Set to keep track of the ext_resource paths we've seen
    scene_lines = scene_content.splitlines()  # Split the scene into individual lines
    cleaned_lines = []

    for line in scene_lines:
        # If the line contains an ext_resource path
        if 'ext_resource path=' in line:
            resource_path_start = line.find('path="') + 6
            resource_path_end = line.find('"', resource_path_start)
            resource_path = line[resource_path_start:resource_path_end]
            
            # If the resource path has been seen before, skip adding this line
            if resource_path in seen_resources:
                continue  # Skip duplicate resource
            
            # Add this resource path to seen resources to avoid future duplicates
            seen_resources.add(resource_path)
        
        # Always add the current line (whether it's a duplicate ext_resource or not)
        cleaned_lines.append(line)

    # Reassemble the scene content without duplicate ext_resources
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene
