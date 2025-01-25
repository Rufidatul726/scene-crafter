@tool
extends EditorPlugin

var dock
var scene_folder := "res://addons/scene-crafter/generated-scene"

func _enter_tree() -> void:
	dock = preload("res://addons/scene-crafter/generate_scene.tscn").instantiate()
	add_control_to_dock(EditorPlugin.DOCK_SLOT_LEFT_UL, dock)


func _exit_tree() -> void:
	remove_control_from_docks(dock)
	dock.free()
