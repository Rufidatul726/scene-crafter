from .remove_duplication import remove_duplicate_lines_from_scene, remove_duplicate_ext_resources
from .ending_check import ensure_nodes_end_with_newline
from .nodes_processing.parent_checking import first_node_remove_parent, nonfirst_node_add_parent
from .nodes_processing.type_checking import is_node_type_valid
from .ext_resouce_processing.ext_resource_process import validate_and_add_ext_resources

def validate(scene_content):
    """Validate the scene content."""
    
    # Remove duplicate lines
    removed_content = remove_duplicate_lines_from_scene(scene_content)
    removed_content = remove_duplicate_ext_resources(removed_content)

    # Ensure that every node ends with a newline
    cleaned_content = ensure_nodes_end_with_newline(removed_content)

    # Remove the parent attribute from the first node
    parent_validated_content = first_node_remove_parent(cleaned_content)
    parent_validated_content = nonfirst_node_add_parent(parent_validated_content)

    # Check if the node type is valid
    node_type_validated_content = is_node_type_valid(parent_validated_content)

    # Missing external resources are handled in a separate function
    ext_resource_validated_content = validate_and_add_ext_resources(node_type_validated_content)

    print(ext_resource_validated_content)
    return ext_resource_validated_content

# # Test the function
# scene_content = """
# [gd_scene load_steps=3 format=2]
# [ext_resource path="res://assets/gelloon.tscn" type="Script" id=1]
# [ext_resource path="res://assets/gelloon.tscn" type="Script" id=2]
# [ext_resource path="res://assets/gelloon.tscn" type="Script" id=3]
# [ext_resource path="res://assets/gelloon.tscn" type="Script" id=4]
# [ext_resource path="res://assets/gelloon.tscn" type="Script" id=5]
# [node name="Godot" type="Godot" parent="."]
# [node name="Godot" type="Node" parent="."]
# [node name="Gelloon" parent="."]
# [node name="Godot" type="Node" parent="."]
# [node name="Godot" parent="."]
# [node name="Godot" type="Button" parent="."]
# [node name="Button" type="Button" parent="."]
# [node name="Gelloon" type="Button" parent="."]
# [node name="Gelloon" parent="."]
# [node name="Gelloon_version = "Gelloon_version = "Version" parent="Godot" parent="."]
# [node name="Gelloon_version = "Version" parent="."]
# [node name="Gelloon_version = "Version" parent="Gelloon_version = "Version" parent="."]
# [node name="Gelloon_version = "Version" parent="."]
# [node name="Gelloon_version = "Version" parent="."]
# [node name="Gelloon_1"]
# [node name="Gelloon_2"]
# [node name="Gelloon_2"]
# [node name="Gelloon_2"]
# [node name="Gelloon_2"]
# [node name="Gelloon_3"]
# [node name="Gelloon_3"]
# [node name="Gelloon_3"]
# [node name="Gelloon_3"]
# [node name="Gelloon
# """
# validate(scene_content)

# # Expected output:
# # [gd_scene load_steps=1 format=2]
# # [node name="Node2D" type="Node2D"]
# # [node name="Sprite" type="Sprite"]