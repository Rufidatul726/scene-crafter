def validate_and_add_ext_resources(scene_content):
    """
    Validate ext_resource paths and types in a Godot .tscn file.
    Updates the resource type or generates a placeholder if mismatched.
    """
    return validate_ext_resource_paths(scene_content, valid_ext_resource_types)

def validate_ext_resource_paths(scene_content, valid_ext_resource_types):
    """
    Validates ext_resource paths and types in a Godot .tscn file.
    Updates the resource type or generates a placeholder if mismatched.
    """
    valid_types_map = {
        item["type"]: item["extensions"] for item in valid_ext_resource_types
    }
    scene_lines = scene_content.splitlines()
    updated_lines = []
    existing_resources = set()
    resource_index = 1
    resource_placeholder = "res://placeholder_script.gd"
    resource_type_placeholder = "Script"

    for line in scene_lines:
        line = line.strip()

        if line.startswith("[ext_resource"):
            # Parse ext_resource
            path_start = line.find('path="') + len('path="')
            path_end = line.find('"', path_start)
            resource_path = line[path_start:path_end]

            type_start = line.find('type="') + len('type="')
            type_end = line.find('"', type_start)
            resource_type = line[type_start:type_end]

            existing_resources.add(resource_path)
            resource_id_start = line.find("id=") + len("id=")
            resource_id_end = line.find("]", resource_id_start)
            resource_id = int(line[resource_id_start:resource_id_end])
            resource_index = max(resource_index, resource_id + 1)

            # Extract file extension from path
            file_extension = resource_path.split(".")[-1] if "." in resource_path else ""

            # Validate type and path
            if resource_type in valid_types_map:
                if not any(resource_path.endswith(ext) for ext in valid_types_map[resource_type]):
                    # print(f"Resource type '{resource_type}' does not match file extension '{file_extension}'. Fixing...")

                    # Try to find a matching type for the extension
                    matched_type = next(
                        (typ for typ, exts in valid_types_map.items() if any(resource_path.endswith(ext) for ext in exts)),
                        None,
                    )
                    if matched_type:
                        # print(f"Changing type '{resource_type}' to '{matched_type}'.")
                        resource_type = matched_type
                    else:
                        # print(f"No valid type found for '{resource_path}'. Using 'Script' as placeholder.")
                        resource_type = "Script"
                        resource_path = "res://placeholder_script.gd"

                # Update the line
                line = f'[ext_resource path="{resource_path}" type="{resource_type}" id={resource_id}]'

            else:
                # Resource type is invalid
                print(f"Invalid resource type '{resource_type}'. Updating to 'Script'.")
                resource_type = "Script"
                resource_path = "res://placeholder_script.gd"
                line = f'[ext_resource path="{resource_path}" type="{resource_type}" id={line.split("id=")[-1]}]'

        updated_lines.append(line)

    # Reassemble the scene content
    updated_scene = "\n".join(updated_lines)
    return updated_scene


# Valid resource types and extensions
valid_ext_resource_types = [
    {"type": "Script", "extensions": [".gd", ".cs"]},
    {"type": "PackedScene", "extensions": [".tscn", ".scn", ".dae"]},
    {"type": "Material", "extensions": [".tres", ".res"]},
    {"type": "Shader", "extensions": [".gdshader", ".tres"]},
    {"type": "Texture", "extensions": [".png", ".jpg", ".jpeg", ".tga", ".bmp", ".exr"]},
    {"type": "Animation", "extensions": [".anim"]},
    {"type": "Mesh", "extensions": [".obj", ".fbx", ".dae", ".glb", ".gltf"]},
    {"type": "Font", "extensions": [".ttf", ".otf", ".fnt"]},
    {"type": "AudioStream", "extensions": [".ogg", ".wav", ".mp3", ".flac"]},
    {"type": "Environment", "extensions": [".tres", ".res"]},
    {"type": "Curve", "extensions": [".tres", ".res"]},
    {"type": "AnimationTree", "extensions": [".tres", ".res"]},
    {"type": "ParticlesMaterial", "extensions": [".tres", ".res"]},
    {"type": "Theme", "extensions": [".tres", ".res"]},
    {"type": "PhysicsMaterial", "extensions": [".tres", ".res"]},
    {"type": "SpriteFrames", "extensions": [".tres", ".res"]},
]