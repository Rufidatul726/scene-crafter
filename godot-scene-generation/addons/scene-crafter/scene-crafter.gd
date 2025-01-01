@tool
extends EditorPlugin

var dock
var scene_folder := "res://scene-crafter-generated-scene"
var log_folder := "user://scene-crafter-logs"

func _enter_tree() -> void:
	dock = preload("res://addons/scene-crafter/generate_scene.tscn").instantiate()
	add_control_to_dock(EditorPlugin.DOCK_SLOT_LEFT_UL, dock)
	ensure_folders_exist()


func _exit_tree() -> void:
	remove_control_from_docks(dock)
	dock.free()

func ensure_folders_exist():
	DirAccess.make_dir_absolute(scene_folder)
	var scene_dir = DirAccess.open(scene_folder)
	if not scene_dir.dir_exists(scene_folder):
		var err := scene_dir.make_dir(scene_folder)
		if err == OK:
			print("Created scene folder at ", scene_folder)
		else:
			print("Failed to create scene folder: ", err)
		
	DirAccess.make_dir_absolute(log_folder)
	var log_dir := DirAccess.open(log_folder)
	if not log_dir.dir_exists(log_folder):
		var err := log_dir.make_dir(log_folder)
		if err == OK:
			print("Created log folder at ", log_folder)
		else:
			print("Failed to create log folder: ", err)
