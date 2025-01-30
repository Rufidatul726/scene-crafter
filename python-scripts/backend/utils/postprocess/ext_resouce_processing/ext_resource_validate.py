def validate_and_add_ext_resources(scene_content):
    """
    Validate ext_resource paths and types in a Godot .tscn file.
    Updates the resource type or generates a placeholder if mismatched.
    """
    scene_content= validate_ext_resource_paths(scene_content, valid_ext_resource_types)
    return assign_resources_to_nodes(scene_content, valid_ext_resource_types)

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

            # Check if resource type is either Texture or Texture2D, and convert it if needed
            if resource_type == "Texture" or resource_type == "Texture2D":
                resource_type = "Texture2D"  # Convert all Texture to Texture2D

            # Validate type and path
            if resource_type in valid_types_map:
                if not any(resource_path.endswith(ext) for ext in valid_types_map[resource_type]):
                    matched_type = next(
                        (typ for typ, exts in valid_types_map.items() if any(resource_path.endswith(ext) for ext in exts)),
                        None,
                    )
                    if matched_type:
                        resource_type = matched_type
                    else:
                        resource_type = "Script"
                        resource_path = "res://placeholder_script.gd"

                # Update the line with the validated/converted type
                line = f'[ext_resource path="{resource_path}" type="{resource_type}" id={resource_id}]'

            else:
                # Resource type is invalid
                print(f"Invalid resource type '{resource_type}'. Updating to 'Script'.")
                resource_type = "Script"
                resource_path = "res://placeholder_script.gd"
                line = f'[ext_resource path="{resource_path}" type="{resource_type}" id={line.split("id=")[-1]}]'

        updated_lines.append(line)

    updated_scene = "\n".join(updated_lines)
    return updated_scene




def assign_resources_to_nodes(scene_data, valid_ext_resource_types):
    import re
    
    # Step 1: Parse resources and nodes
    resources = {}
    node_lines = []
    existing_nodes = {}
    node_textures = {}
    
    ext_resource_pattern = re.compile(r'\[ext_resource path="(.*?)" type="(.*?)" id=(\d+)\]')
    node_pattern = re.compile(r'\[node name="(.*?)" type="(.*?)" parent=".*?"\]')
    
    lines = scene_data.strip().split('\n')
    updated_lines = []
    node_insert_indices = {}
    
    for i, line in enumerate(lines):
        res_match = ext_resource_pattern.match(line)
        node_match = node_pattern.match(line)
        
        if res_match:
            path, res_type, res_id = res_match.groups()
            res_id = int(res_id)
            resources[res_id] = {'path': path, 'type': res_type, 'used': False}
            updated_lines.append(line)
        elif node_match:
            node_name, node_type = node_match.groups()
            existing_nodes[node_name] = node_type
            node_lines.append((node_name, node_type))
            updated_lines.append(line)
            node_insert_indices[node_name] = len(updated_lines)
        else:
            if "ExtResource(" in line:
                last_node_name = node_lines[-1][0] if node_lines else None
                if last_node_name:
                    node_textures[last_node_name] = True
            updated_lines.append(line)
    
    # Step 2: Assign resources correctly after respective nodes or create new nodes
    assigned_resources = {}
    new_nodes = []
    
    for res_id, res in resources.items():
        res_type = res['type']
        best_node = None
        
        for category in valid_ext_resource_types:
            if category['type'] == res_type:
                for option in category['nodes']:
                    for node_name, node_type in node_lines:
                        if option['node'] == node_type and node_name not in assigned_resources.values():
                            if node_name not in node_textures:  # Ensure each node gets only one texture
                                best_node = node_name
                                assigned_resources[res_id] = node_name
                                node_textures[node_name] = True
                                break
                    if best_node:
                        break
            if best_node:
                break
        
        if best_node and best_node in node_insert_indices:
            insert_index = node_insert_indices[best_node]
            updated_lines.insert(insert_index, f'Texture2D = ExtResource({res_id})')
        else:
            # Create a new node if no suitable one exists
            for category in valid_ext_resource_types:
                if category['type'] == res_type:
                    new_node_type = category['nodes'][0]['node']  # Take the highest precedence node type
                    new_node_name = f"Auto_{new_node_type}_{res_id}"
                    new_node_line = f'[node name="{new_node_name}" type="{new_node_type}" parent="."]'
                    new_nodes.append(new_node_line)
                    new_nodes.append(f'Texture2D = ExtResource({res_id})')
                    break
    
    updated_lines.extend(new_nodes)
    
    return '\n'.join(updated_lines)


# Valid resource types and extensions
valid_ext_resource_types = [
    {"type": "Script", "extensions": [".gd", ".cs"], "nodes": [
        {"node": "Script", "precedence": 1},
        {"node": "Node2D", "precedence": 2},
        {"node": "Node3D", "precedence": 3},
        {"node": "Control", "precedence": 4}
    ]},
    {"type": "PackedScene", "extensions": [".tscn", ".scn", ".dae"], "nodes": [
        {"node": "PackedScene", "precedence": 1},
        {"node": "Node2D", "precedence": 2},
        {"node": "Node3D", "precedence": 3}
    ]},
    {"type": "Material", "extensions": [".tres", ".res"], "nodes": [
        {"node": "Material", "precedence": 1},
        {"node": "ShaderMaterial", "precedence": 2},
        {"node": "MeshInstance", "precedence": 3}
    ]},
    {"type": "Shader", "extensions": [".gdshader", ".tres"], "nodes": [
        {"node": "Shader", "precedence": 1},
        {"node": "ShaderMaterial", "precedence": 2}
    ]},
    {"type": "Texture2D", "extensions": [".png", ".jpg", ".jpeg", ".tga", ".bmp", ".exr"], "nodes": [
        {"node": "Sprite2D", "precedence": 1},
        {"node": "Light2D", "precedence": 2},
        {"node": "ParticleSystem", "precedence": 3}
    ]},
    {"type": "Animation", "extensions": [".anim"], "nodes": [
        {"node": "AnimationPlayer", "precedence": 1},
        {"node": "AnimationTree", "precedence": 2}
    ]},
    {"type": "Mesh", "extensions": [".obj", ".fbx", ".dae", ".glb", ".gltf"], "nodes": [
        {"node": "MeshInstance", "precedence": 1},
        {"node": "ImmediateGeometry", "precedence": 2},
        {"node": "GridMap", "precedence": 3}
    ]},
    {"type": "Font", "extensions": [".ttf", ".otf", ".fnt"], "nodes": [
        {"node": "Font", "precedence": 1},
        {"node": "Label", "precedence": 2},
        {"node": "Button", "precedence": 3}
    ]},
    {"type": "AudioStream", "extensions": [".ogg", ".wav", ".mp3", ".flac"], "nodes": [
        {"node": "AudioStreamPlayer", "precedence": 1},
        {"node": "AudioStreamPlayer2D", "precedence": 2},
        {"node": "AudioStreamPlayer3D", "precedence": 3}
    ]},
    {"type": "Environment", "extensions": [".tres", ".res"], "nodes": [
        {"node": "Environment", "precedence": 1},
        {"node": "WorldEnvironment", "precedence": 2}
    ]},
    {"type": "Curve", "extensions": [".tres", ".res"], "nodes": [
        {"node": "Curve", "precedence": 1},
        {"node": "Path", "precedence": 2}
    ]},
    {"type": "AnimationTree", "extensions": [".tres", ".res"], "nodes": [
        {"node": "AnimationTree", "precedence": 1},
        {"node": "AnimationPlayer", "precedence": 2}
    ]},
    {"type": "ParticlesMaterial", "extensions": [".tres", ".res"], "nodes": [
        {"node": "ParticlesMaterial", "precedence": 1},
        {"node": "Material", "precedence": 2}
    ]},
    {"type": "Theme", "extensions": [".tres", ".res"], "nodes": [
        {"node": "Theme", "precedence": 1},
        {"node": "Control", "precedence": 2}
    ]},
    {"type": "PhysicsMaterial", "extensions": [".tres", ".res"], "nodes": [
        {"node": "PhysicsMaterial", "precedence": 1},
        {"node": "RigidBody", "precedence": 2},
        {"node": "StaticBody", "precedence": 3}
    ]},
    {"type": "SpriteFrames", "extensions": [".tres", ".res"], "nodes": [
        {"node": "SpriteFrames", "precedence": 1},
        {"node": "AnimationPlayer", "precedence": 2}
    ]}
]