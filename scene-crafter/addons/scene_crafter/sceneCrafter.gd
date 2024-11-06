# copilot_plugin.gd
@tool
extends EditorPlugin

var dock
var http_request
var api_key = "" # You'll need to set this up in the settings
const SETTINGS_PATH = "scene)crafter/settings/api_key"

func _enter_tree():
	# Initialize the dock
	dock = preload("res://addons/copilot/copilot_dock.tscn").instantiate()
	add_control_to_dock(DOCK_SLOT_RIGHT_UL, dock)
	
	# Add plugin settings
	add_autoload_singleton("SceneCrafter", "res://addons/scene_crafter/sceneCrafter.gd")
	
	# Add plugin settings
	if ProjectSettings.has_setting(SETTINGS_PATH):
		api_key = ProjectSettings.get_setting(SETTINGS_PATH)
	else:
		ProjectSettings.set_setting(SETTINGS_PATH, "")
		ProjectSettings.set_initial_value(SETTINGS_PATH, "")
		
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)

func _exit_tree():
	remove_control_from_docks(dock)
	dock.free()
	remove_autoload_singleton("CopilotHelper")
