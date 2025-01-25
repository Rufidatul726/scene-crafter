def first_node_remove_parent(scene_content):
    """Remove the parent attribute from the first node in the scene."""
    # Split the scene content into individual lines
    scene_lines = scene_content.splitlines()
    cleaned_lines = []
    first_node = True

    for line in scene_lines:
        # Skip lines that don’t meet our conditions
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # If it's the first node, remove the parent attribute
        if first_node and line.startswith("[node"):
            if "parent=" in line:
                line = line.replace(' parent="."', "")
            first_node = False

        cleaned_lines.append(line)

    # Reassemble the scene content
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene

def nonfirst_node_add_parent(scene_content):
    """Add a parent attribute to all nodes except the first node in the scene."""
    # Split the scene content into individual lines
    scene_lines = scene_content.splitlines()
    cleaned_lines = []
    first_node = True

    for line in scene_lines:
        # Skip lines that don’t meet our conditions
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # If it's the first node, remove the parent attribute
        if first_node and line.startswith("[node"):
            first_node = False

        # If it's not the first node, add the parent attribute if it's missing at the end of the line
        elif not first_node and line.startswith("[node") and line.endswith("]"):
            if "parent=" not in line:
                # Add parent attribute to the node
                line = line.replace("]", " parent=\".\"]")

        cleaned_lines.append(line)

    # Reassemble the scene content
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene