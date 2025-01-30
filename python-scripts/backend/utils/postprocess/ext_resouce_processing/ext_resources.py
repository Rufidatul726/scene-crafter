import os
from pathlib import Path

def check_and_handle_invalid_resources(scene_content, path):
    """Check for invalid external resources, remove them if not used, or create them if referenced."""

    # First, parse existing external resources from the scene content
    scene_lines = scene_content.splitlines()
    ext_resources = {}  # Key: resource path, Value: resource id
    new_scene_lines = []  # Will store updated scene content without removed lines

    for line in scene_lines:
        line = line.strip()
        if line.startswith("[ext_resource"):
            path_start = line.find('path="') + len('path="')
            path_end = line.find('"', path_start)
            resource_path = line[path_start:path_end]
            resource_id = str(line.split("id=")[1].split()[0])  # Extract resource id
            ext_resources[resource_path] = resource_id

    # Now, check for references to these resources in nodes
    used_resources = set()
    for line in scene_lines:
        line = line.strip()
        if line.startswith("[node") or line.startswith("[sub_resource"):
            for resource_path, resource_id in ext_resources.items():
                if f"ExtResource({resource_id})" in line:
                    used_resources.add(resource_path)

    # Remove invalid external resources or create missing resources
    for line in scene_lines:
        line_stripped = line.strip()
        if line_stripped.startswith("[ext_resource"):
            # Extract resource path
            path_start = line_stripped.find('path="') + len('path="')
            path_end = line_stripped.find('"', path_start)
            resource_path = line_stripped[path_start:path_end]

            # Check if resource is valid
            resource_path_abs = Path(path + resource_path[5:]  ) # Strip 'res://' and join with base path
            if resource_path not in used_resources and not resource_path_abs.exists():
                # Skip adding this line (removes unused + missing resources)
                continue
            elif not resource_path_abs.exists():
                # Create missing resource file if referenced by a node
                resource_path_abs.parent.mkdir(parents=True, exist_ok=True)
                with open(resource_path_abs, 'w') as f:
                    f.write("# Placeholder content for missing resource")
            else:
                continue

        # Keep all lines except removed `[ext_resource]` lines
        new_scene_lines.append(line)

    return "\n".join(new_scene_lines)


def find_resources(path, prompt):
    """ Extract resource-related keywords from the given prompt."""
    
    exclude_ext = [".tscn", ".gd", ".import", ".cfg", ".md5", ".ctex", "scene", "script", "res://"]
    
    matching_files = []
    relative_paths = []

    prompt_words = set(prompt.lower().split())

    for file in Path(path).rglob('*'):
        if file.is_file() and file.suffix not in exclude_ext:
            # Get file name without extension
            file_name = file.stem.lower()
            words = file_name.split("_")
            words.extend(file_name.split("-"))
            words.extend(file_name.split(" "))
            
            if any(word in words for word in prompt_words):
                matching_files.append(file.resolve())
                relative_paths.append(f"res://{file.relative_to(path).as_posix()}")

    return relative_paths


def find_if_the_ext_resouce_is_added(scene_content, path, prompt):
    """Check if the external resources are added to the scene content."""
    relative_paths = find_resources(path, prompt)
    scene_lines = scene_content.splitlines()
    existing_resources = set()

    for line in scene_lines:
        line = line.strip()

        if line.startswith("[ext_resource"):
            # Parse ext_resource
            path_start = line.find('path="') + len('path="')
            path_end = line.find('"', path_start)
            resource_path = line[path_start:path_end]
            existing_resources.add(resource_path)

    # Check for missing resources
    missing_resources = [resource for resource in relative_paths if resource not in existing_resources]

    if missing_resources:
        # Find the section where we can add the missing resources (before the first node section, if possible)
        for i, line in enumerate(scene_lines):
            if line.startswith("[node"):
                insert_index = i
                break
        else:
            insert_index = len(scene_lines)

        # Add missing resources before that section
        for missing_resource in missing_resources:
            # Create a new [ext_resource] entry for each missing resource
            ext_resource_line = f'[ext_resource path="{missing_resource}" type="Texture" id={len(existing_resources) + 1}]'
            scene_lines.insert(insert_index, ext_resource_line)
            existing_resources.add(missing_resource)

    # Join the lines back into a single string
    updated_scene_content = "\n".join(scene_lines)
    return updated_scene_content