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