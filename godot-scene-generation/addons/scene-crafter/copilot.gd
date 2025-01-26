@tool
extends Control

var last_opened_file: String = ""  # Tracks the last active file or scene
var timer: Timer  # Timer for global polling

func _enter_tree():
	print("CoPilot Initialized!")
	_start_polling_global_changes()
	connect_signals()

func _exit_tree():
	_stop_polling_global_changes()
	disconnect_signals()
	print("CoPilot Disabled.")

# Timer polling for both active scene and global project changes
func _start_polling_global_changes():
	if not timer:
		timer = Timer.new()
		timer.wait_time = 0.5  # Half a second polling interval
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
	filesystem.connect("filesystem_changed", Callable(self, "_on_filesystem_changed"))

func disconnect_signals():
	#var editor_interface = get_editor_interface()
	var filesystem = EditorInterface.get_resource_filesystem()
	if filesystem.is_connected("filesystem_changed", Callable(self, "_on_filesystem_changed")):
		filesystem.disconnect("filesystem_changed", Callable(self, "_on_filesystem_changed"))

# Handle the "filesystem changed" signal (e.g., new files, changes)
func _on_filesystem_changed():
	print("Filesystem has changed. Re-analyzing...")
	_poll_global_changes()

# Track active scene and output on change
func _check_active_scene():
	var scene_tree = get_tree()
	if scene_tree and scene_tree.current_scene:
		var current_scene_path = scene_tree.current_scene.filename
		if current_scene_path != last_opened_file:
			print("Scene changed to:", current_scene_path)
			last_opened_file = current_scene_path

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
