
def is_node_type_valid(scene_content):
    """Check if the node type is valid."""
    valid_node_types = [
        "Node", "Node2D", "CanvasItem", "Control", "Node3D", "HBoxContainer", "VBoxContainer", "Container",
        "CanvasModulate", "CanvasLayer", "WorldEnvironment", "GraphEdit",
        "GraphNode", "ProgressBar", "Range", "Range2D", "Range3D",
        "Spatial", "Camera3D", "MeshInstance3D", "Skeleton3D", "AnimationPlayer", 
        "DirectionalLight3D", "OmniLight3D", "SpotLight3D", "Environment", "Sprite3D", 
        "FogVolume", "Particles3D", "Viewport",
        "Sprite2D", "AnimatedSprite2D", "TileMap", "Light2D", "Polygon2D", 
        "NinePatchRect", "TextureRect", "Label", "Button", "ColorRect", 
        "Line2D", "Particles2D",
        "StaticBody2D", "KinematicBody2D", "CharacterBody2D", "RigidBody2D",
        "StaticBody3D", "KinematicBody3D", "CharacterBody3D", "RigidBody3D",
        "CollisionShape2D", "CollisionPolygon2D", "CollisionShape3D", "CollisionPolygon3D",
        "AudioStreamPlayer", "AudioStreamPlayer2D", "AudioStreamPlayer3D", "AudioListener", 
        "AudioBusLayout",
        "Window", "Popup", "PopupPanel", "TextureButton", "OptionButton", 
        "TabContainer", "HSlider", "VSlider", "SpinBox", "HScrollBar", "VScrollBar", 
        "TextEdit", "LineEdit", "RichTextLabel",
        "Camera2D", "Camera3D",
        "AnimationPlayer", "AnimationTree",
        "ShaderMaterial", "SkyMaterial", "ShaderEffect",
        "LightOccluder2D", "VisibilityNotifier2D", "VisibilityNotifier3D", "ViewportTexture"
    ]

    scene_lines = scene_content.splitlines()
    cleaned_lines = []

    fallback_node_type = "Node"
    
    for line in scene_lines:
        line = line.strip()

        # Check for node lines and validate node types
        if line.startswith("[node"):
            # Extract type from `type="..."` in the line
            type_index = line.find('type="')
            if type_index != -1:
                # Extract node type
                type_start = type_index + len('type="')
                type_end = line.find('"', type_start)
                node_type = line[type_start:type_end]

                if node_type not in valid_node_types:
                    # print(f"Invalid node type '{node_type}' found. Replacing with '{fallback_node_type}'.")
                    # Replace the invalid type with the fallback type
                    line = line[:type_start] + fallback_node_type + line[type_end:]
            else:
                # Add type if missing
                # print(f"Missing type in node: {line}. Adding type '{fallback_node_type}'.")
                line = line[:-1] + f' type="{fallback_node_type}"]'

        # If the line passes all validations, keep it
        cleaned_lines.append(line)

    # Reassemble the scene content
    cleaned_scene = "\n".join(cleaned_lines)
    return cleaned_scene