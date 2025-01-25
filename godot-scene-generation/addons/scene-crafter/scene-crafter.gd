@tool
extends EditorPlugin

var dock
var scene_folder := "res://addons/scene-crafter/generated-scene"

@export var api_url : String = "https://api.groq.com/openai/v1/chat/completions"
var api_key : String 

var http_request : HTTPRequest
var prompt_input : TextEdit
var response_label : Label

func _enter_tree() -> void:
	dock = preload("res://addons/scene-crafter/generate_scene.tscn").instantiate()
	add_control_to_dock(EditorPlugin.DOCK_SLOT_LEFT_UL, dock)
	
	start_monitoring()

func _exit_tree() -> void:
	remove_control_from_docks(dock)
	dock.free()

def start_monitoring():
	
