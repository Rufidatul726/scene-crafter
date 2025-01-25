def get_template(template_name):
    SYSTEM_TEMPLATE = """The code should be for Godot Engine. do not give me steps.
    If the user is asking for generating a scene, you should create a .tscn file.  like this:
    ```
    [gd_scene load_steps=2 format=2]
    [sub_resource type="PackedScene" id=1]
    resource_name = "Main"
    class_name = "Node"
    ```
    If the user is asking for generating a script, you should create a .gd file. like this:
    ```
    extends Node

    func _ready():
        my_var = 5

    func _process(delta):
        if Input.is_action_pressed("ui_right"):
        
    ```
    If the user is asking for correcting an error, you should provide the corrected code in that godot {version}.
    If the user is asking for a tutorial, you should provide a step-by-step guide.
    If the user is asking for a code snippet, you should provide a code snippet.
    If the user is asking for a code explanation, you should provide an explanation of the code.
    """

    TSCN_TEMPLATE = """The code should be for Godot Engine for {version}. Generate .tscn file"""

    GD_TEMPLATE = """The code should be for Godot Engine for {version}. Generate .gd file"""

    ERROR_TEMPLATE = """The code should be for Godot Engine for {version}. Correct the error in the code"""

    if template_name == "system":
        return SYSTEM_TEMPLATE
    elif template_name == "tscn":
        return TSCN_TEMPLATE
    elif template_name == "gd":
        return GD_TEMPLATE
    elif template_name == "error":
        return ERROR_TEMPLATE
    else:
        return SYSTEM_TEMPLATE

def get_node_type():
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

    return valid_node_types

def get_ext_res_type():
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
        {"type": "SpriteFrames", "extensions": [".tres", ".res"]}
    ]

    return valid_ext_resource_types