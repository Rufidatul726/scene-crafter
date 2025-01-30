@tool
extends EditorPlugin

const starting_gdscript: String = "the code should be in gdscript for godot game engine"
const ending_gdscript: String= "you should complete the code. no extra conversation"
const REQUEST_COOLDOWN: float = 30.0  # 3 minutes
const FILE_REQUEST_COOLDOWN: float = 50.0  # 15 minutes

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

var cooldown_timer: Timer
var can_request: bool = true
var file_request_tracker: Dictionary = {}  # Tracks last request times for individual files

var flag=true
var acceptKey: bool

var code_editor: CodeEdit
var prevCode
var newCode

func _enter_tree() -> void:
	dock = preload("res://addons/scene-crafter/generate_scene.tscn").instantiate()
	add_control_to_dock(EditorPlugin.DOCK_SLOT_LEFT_UL, dock)
	
	_start_polling_global_changes()
	connect_signals()
	
	cooldown_timer = Timer.new()
	cooldown_timer.wait_time = 180  # 3 minutes in seconds
	cooldown_timer.one_shot = true
	cooldown_timer.connect("timeout", Callable(self, "_on_cooldown_finished"))
	add_child(cooldown_timer)
	
	#http_request = HTTPRequest.new()
	#add_child(http_request)
	#http_request.connect("request_completed", Callable(self, "_on_request_completed"))
	
	#copilot= preload("res://addons/scene-crafter/copilot.tscn").instantiate()
	#add_control_to_dock(EditorPlugin.DOCK_SLOT_RIGHT_BR, copilot)
	#copilot.hide()
	#start_monitoring()
	

func _exit_tree() -> void:
	remove_control_from_docks(dock)
	dock.free()
	
	if(copilot!=null):
		remove_control_from_docks(copilot)
		copilot.free()
		
	cooldown_timer.queue_free()
	http_request.queue_free()
	_stop_polling_global_changes()
	disconnect_signals()
	print("CoPilot Disabled.")
	
func start_monitoring():
	if can_request:
		# Initiate the request only if the cooldown has finished
		can_request = false
		http_request= HTTPRequest.new()
		add_child(http_request)
		http_request.connect("request_completed", Callable(self, "_on_request_completed_on_monitor"))
	
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

func _on_request_completed_on_monitor(result, response_code, headers, body) -> void:
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
	if opened_file and opened_file != last_opened_file and opened_file!= "":
		print("Opened file switched to:", opened_file)
		last_opened_file = opened_file
		var current_time = Time.get_time_dict_from_system()
		_make_request_for_file(opened_file)

# Determine if a request is allowed for a file
func _make_request_for_file(file_path: String):
	var current_time = Time.get_unix_time_from_system()
	print("current time= ")
	print(current_time)
	if file_request_tracker.has(file_path):
		if current_time - file_request_tracker[file_path] < FILE_REQUEST_COOLDOWN:
			print("Skipping request for file '%s'. Last request was less than 15 minutes ago." % file_path)
			return
	# If no cooldown or allowed, send the request
	if can_request:
		file_request_tracker[file_path] = current_time
		_send_http_request(file_path)
	else:
		print("Global cooldown active. Wait for %s seconds before the next request." % REQUEST_COOLDOWN)

# Send HTTP request for the opened file
func _send_http_request(file_path: String):
	var filecontent
	var file= FileAccess.open(file_path, FileAccess.READ)
	if file:
		print("File opened successfully")
		filecontent= file.get_as_text()
		file.close()
		var body = {
			"message":  starting_gdscript +
					" Generate data for filedata: %s"  % filecontent
					+ ending_gdscript
			#"model": "llama-3.3-70b-versatile"
		}
		var json_body = JSON.stringify(body)
		
		var headers = {
			"Content-Type": "application/json", # Replace with the desired content type
			"Authorization": "Bearer YOUR_ACCESS_TOKEN" # Replace 'YOUR_ACCESS_TOKEN' with your actual token
		}
		
		http_request= HTTPRequest.new()
		add_child(http_request)
		http_request.connect("request_completed", Callable(self, "_on_request_completed"))

		http_request.request(
			"http://localhost:8001/recommend/",
			["Content-Type: application/json"],
			HTTPClient.METHOD_POST,
			json_body
		)
		
		can_request = false
		cooldown_timer.start()

func _on_request_completed(result: int, response_code: int, headers: Array, body) -> void:
	# Parse the response
	var response = JSON.parse_string(body.get_string_from_utf8())

	if response_code == 200:
		print("Response received:", response)
		
		# Extract the code content
		if response.has("response"):
			var script_code: String = response["response"]
			var start_index = script_code.find("```")
			 # Find the position of the first occurrence of "extends" or "@"
			var extend_index = script_code.find("extends")
			var at_index = script_code.find("@")
			script_code = script_code.strip_edges()  # First remove general whitespace from both ends
			var first_index = script_code.find("```")
			var first_extend_index= script_code.find("extends")
			var first_at_index=script_code.find("@")
			
			var start_index_at_extendorat = -1

			# Determine which comes first ("extends" or "@")
			if extend_index != -1 and (at_index == -1 or extend_index < at_index):
				start_index_at_extendorat = extend_index  # "extends" found
			elif at_index != -1:
				start_index_at_extendorat = at_index  # "@" found
			
			if first_index != -1:
				# Find the position of the second occurrence of "```"
				var second_index = script_code.find("```", first_index + 3)  # Starting search after the first "```"

				if second_index != -1:
					# Extract the substring between the first and second "```"
					script_code = script_code.substr(first_index + 3, second_index - first_index - 3)

					# Optionally, remove any trailing "```" or unwanted characters at the end
					script_code = script_code.strip_edges()

					if script_code != "":
						# Write the code to the last opened file
						print(last_opened_file)
						if last_opened_file != "":
							#_replace_file_content(last_opened_file, script_code)
							_insert_code_suggestion(last_opened_file, script_code)
					else:
						print("No file is currently open to replace content.")
				else:
					print("Second ``` not found in the string.")
			elif start_index_at_extendorat!= -1:
				pass
			else:
				print("could not start to make script from the string.")
		else:
			print("Response does not contain a 'response' field.")
	else:
		print("Request failed with code %s: %s" % [response_code, response])

# Highlight Differences Between Old and New Code
func highlight_suggestions(old_code: String, suggested_code: String, editor_script) -> String:
	var old_lines = old_code.split("\n")
	var new_lines = suggested_code.split("\n")
	var highlighted_text = ""

	# Compare old and new lines
	for i in range(max(old_lines.size(), new_lines.size())):
		if i < old_lines.size() and i < new_lines.size():
			# Check if lines are the same
			if old_lines[i] == new_lines[i]:
				highlighted_text += old_lines[i]
			else:
				highlighted_text += old_lines[i]  # Old line in red
				editor_script.set_line_background_color(editor_script.get_caret_line(), Color.DARK_GRAY)
				highlighted_text += new_lines[i]  # Suggested line in green
		elif i < old_lines.size():
			# Remaining lines in old code
			highlighted_text += old_lines[i] 
		elif i < new_lines.size():
			# Remaining lines in new code
			editor_script.set_line_background_color(editor_script.get_caret_line(), Color.DARK_GRAY)
			highlighted_text +=  new_lines[i] 

	return highlighted_text
	
func _replace_file_content(file_path: String, new_content: String) -> void:
	var file := FileAccess.open(file_path, FileAccess.WRITE)
	if file:
		file.store_string(new_content)
		file.close()
		print("File content replaced successfully: %s" % file_path)
	else:
		print("Failed to open file '%s' for writing. Error code: %s" % [file_path, file])

func _insert_code_suggestion(file_path: String, suggested_code: String) -> void:
	var editor_script = EditorInterface.get_script_editor().get_current_editor().get_base_editor()
	if not editor_script:
		print("No active editor found.")
		return

	# Get current caret position (where the suggestion should appear)
	var caret_pos = editor_script.get_caret_line()
	var caret_index= editor_script.get_caret_index_edit_order()
	var code = editor_script.get_text_for_code_completion()
	
	editor_script.set_code_hint(suggested_code)
	editor_script.set_caret_line(0)
	#editor_script.set_caret_line(caret_pos + comment_block.length())  # Move the caret after the suggestion
	
	var ketacpt= InputEventKey.new()
	if ketacpt.pressed==true and ketacpt.keycode==4194326:
		print("key pressed...")
		editor_script.set_code_hint_draw_below(true)
		print("drew")

	editor_script.set_line(caret_pos, newCode, code_editor)
	print("set line not worked")
	print("Code suggestion inserted at the caret position.")
	prevCode= code
	newCode= highlight_suggestions(code, suggested_code, editor_script)
	
	code_editor= CodeEdit.new()
	code_editor.code_completion_enabled= true
	code_editor.connect("code_completion_requested", Callable(self, "_request_code_completion"))
	print("code_editor not worked")
	
	#code_editor.code_completion_requested.connect(_request_code_completion)
	
func _request_code_completion(force):
	print(force)
	print(CodeEdit.KIND_FUNCTION)
	code_editor.add_code_completion_option(CodeEdit.KIND_FUNCTION, prevCode, newCode, highlight_color)
	code_editor.update_code_completion_options(force)
		
func get_code_editor():
	var script_editor = EditorInterface.get_script_editor()
	if script_editor:
		return script_editor.get_current_editor().get_base_editor()
	return null
	
# Get the currently opened script or file
func _get_opened_file() -> String:
	var script_editor = EditorInterface.get_script_editor()
	if script_editor:
		var current_script = script_editor.get_current_script()
		if current_script:
			return current_script.resource_path
	return ""

func _on_cooldown_finished() -> void:
	# Reset the flag when the cooldown finishes
	can_request = true
	print("Cooldown period finished. You can now make another request.")
