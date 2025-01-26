@tool
extends EditorPlugin

const starting_gdscript: String = "the code should be in gdscript for godot game engine"
const ending_gdscript: String= "you should complete rest of the code. no extra conversation"

var dock
var scene_folder := "res://addons/scene-crafter/generated-scene"

var url : String = ""
var api_url: String = ""
var api_key : String = ""
var isGenerated = []
@export var highlight_color: Color = Color(0.8, 0.8, 0, 0.3)
var current_highlight = null

var http_request : HTTPRequest
var prompt_input : TextEdit
var response_label : Label
var copilot


var last_opened_file: String = ""  # Tracks the last active file 
var last_scene_file: String= "" # Tracks the last active scene
var timer: Timer  # Timer for global polling

var flag=true

func _enter_tree() -> void:
	dock = preload("res://addons/scene-crafter/generate_scene.tscn").instantiate()
	add_control_to_dock(EditorPlugin.DOCK_SLOT_LEFT_UL, dock)
	
	_start_polling_global_changes()
	connect_signals()
	
	#start_monitoring()

func _exit_tree() -> void:
	remove_control_from_docks(dock)
	dock.free()
	
	_stop_polling_global_changes()
	disconnect_signals()
	print("CoPilot Disabled.")
	
	#if(copilot || flag):
		#copilot._exit_tree()
	
func start_monitoring():
	http_request= HTTPRequest.new()
	add_child(http_request)
	http_request.connect("request_completed", Callable(self, "_on_request_completed"))
	
	var body = {
		"messages": [
		{
			"role": "user",
			"content": prompt_input
		}
		],
		"model": "llama-3.3-70b-versatile"
	}
	
	var json_body = JSON.stringify(body)
	
	http_request.request(
		"http://127.0.0.1:8000/getdir/",
		["Content-Type: application/json",
		"Authorization: Bearer %s" % api_key], # Headers
		HTTPClient.METHOD_POST,
		
	)

func _on_request_completed(result, response_code, headers, body) -> void:
	var response = JSON.parse_string(body.get_string_from_utf8())
	if response_code == 200:
		print("Response from Python:", response)
	else:
		print("Error:", response_code, response)
	

# Timer polling for both active scene and open file changes
# Timer polling for both active scene and global project changes
func _start_polling_global_changes():
	if not timer:
		timer = Timer.new()
		timer.wait_time = 10  # ten second polling interval
		timer.autostart = true
		timer.connect("timeout", Callable(self, "_poll_global_changes"))
		add_child(timer)
	timer.start()

func _stop_polling_global_changes():
	if timer:
		timer.stop()
		timer.queue_free()
		timer = null

# Handle global events such as file or scene switches
func _poll_global_changes():
	_check_active_scene()
	_check_opened_file()

# Listen for relevant editor events
func connect_signals():
	#var editor_interface = EditorInterface
	var filesystem = EditorInterface.get_resource_filesystem()
	var scenesystem = EditorInterface.get_open_scenes()
	filesystem.connect("filesystem_changed", Callable(self, "_on_filesystem_changed"))
	scenesystem.connect("scenesystem_changed", Callable(self, "_on_scenesystem_changed"))

func disconnect_signals():
	#var editor_interface = get_editor_interface()
	var filesystem = EditorInterface.get_resource_filesystem()
	var scenesystem = EditorInterface.get_open_scenes()
	if filesystem.is_connected("filesystem_changed", Callable(self, "_on_filesystem_changed")):
		filesystem.disconnect("filesystem_changed", Callable(self, "_on_filesystem_changed"))
	if scenesystem.is_connected("scenesystem_changed", Callable(self, "_on_scenesystem_changed")):
		scenesystem.disconnect("scenesystem_changed", Callable(self, "_on_scenesystem_changed"))

# Handle the "filesystem changed" signal (e.g., new files, changes)
func _on_filesystem_changed():
	print("Filesystem has changed. Re-analyzing...")

func _on_scenesystem_changed():
	print("Scenesystem has changed. Re-analyzing...")

# Track active scene and output on change
func _check_active_scene():
	var scene_tree = EditorInterface.get_open_scenes()
	if scene_tree and scene_tree.size()>0:
		var current_scene_path = scene_tree[scene_tree.size() - 1]
		if current_scene_path != last_scene_file:
			print("Scene changed to:", current_scene_path)
			last_scene_file = current_scene_path

# Track opened file changes and output on change
func _check_opened_file():
	var opened_file = _get_opened_file()
	if opened_file and opened_file != last_opened_file:
		print("Opened file switched to:", opened_file)
		last_opened_file = opened_file
		
		

# Get the currently opened script or file
func _get_opened_file() -> String:
	var script_editor = EditorInterface.get_script_editor()
	if script_editor:
		var current_script = script_editor.get_current_script()
		if current_script:
			return current_script.resource_path
	return ""
