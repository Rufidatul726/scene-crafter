@tool
extends Control

@onready var input= $VBoxContainer/HBoxContainer/TextEdit
@onready var sendButton= $VBoxContainer/HBoxContainer/SendButton
@onready var trainButton = $VBoxContainer/MainMenu/train

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	sendButton.connect("pressed", Callable(self, "_on_SubmitButton_pressed"))
	
	trainButton.connect("pressed", Callable( self, "_on_train_pressed"))

func _on_train_pressed() -> void:
	var trainScript= preload("res://addons/scene-crafter/train.gd").new()
	trainScript._on_train_button_pressed()

func _on_send_button_pressed() -> void:
	var text_input = input.text 
	print("User input:", text_input)
	var version_info = Engine.get_version_info() 
	print("Godot Version: %s.%s.%s" % [version_info["major"], version_info["minor"], version_info["patch"]])
	
	var json_data = {
		"prompt": text_input,
		"path": ProjectSettings.globalize_path("res://"), 
		"version": version_info["major"]
	}
	
	var scene_path= "res://scene-crafter-generated-scene/main.tscn"
	
	var http := HTTPRequest.new()
	add_child(http)
	http.connect("request_completed", Callable(self, "_on_request_completed"))
	
	http.request(
		"http://127.0.0.1:8000/generate_scene/",  # Your Python server endpoint
		["Content-Type: application/json"], # Headers
		HTTPClient.METHOD_POST,
		JSON.stringify(json_data)
	)
	
func _on_request_completed(result, response_code, headers, body) -> void:
	var response = JSON.parse_string(body.get_string_from_utf8())
	if response_code == 200:
		print("Response from Python:", response)
		
		# Assuming the 'file' path is in the response:
		var file_path = response["file"]
		
		# Open the file to inspect its contents
		var file = FileAccess.open(file_path, FileAccess.READ)
		if file:
			var scene_data = file.get_as_text()  # Load scene data as a string
			file.close()  # Close the file after reading
			
			# Now, check external resources in the scene
			var external_resources = get_external_resources(scene_data)
			print(external_resources)
			for resource_path in external_resources:
				# Create a resource UID for each external resource
				var resource_uid = create_resource_uid(resource_path)
				print("Resource UID for ", resource_path, " is ", resource_uid)
				
				# Here you would import the resource or handle it as needed
				import_resource(resource_path, resource_uid)
				
		else:
			print("Failed to open the file.")
	else:
		print("Error:", response_code, response)

# Helper function to extract external resources from the scene data
func get_external_resources(scene_data: String) -> Array:
	var resources = []
	
	# Split the scene data into lines
	var lines = scene_data.split("\n")
	
	# Iterate through each line to find external resource lines
	for line in lines:
		if line.begins_with("[ext_resource"):
			# Extract the resource path from the line
			var path_start = line.find("path=\"") + 6  # Find where the path starts (after "path = \"")
			var path_end = line.find("\"", path_start)  # Find the closing quote of the path
			if path_start != -1 and path_end != -1:
				var resource_path = line.substr(path_start, path_end - path_start)
				print(resource_path)
				# Add the resource path to the list if it's not already present
				if resource_path.begins_with("res://") and not resources.has(resource_path):
					resources.append(resource_path)
	
	return resources


# Recursive function to extract resources from nodes
func extract_resources_from_node(node, resources: Array) -> void:
	# Check all properties of the node
	for property in node.get_property_list():
		var value = node.get(property.name)
		
		if value is String and value.begins_with("res://"):  # Assuming resources are prefixed with "res://"
			print("Hello")
			if not resources.has(value):
				resources.append(value)
		
		# If the value is a resource type, recursively check the properties of the resource
		if value is Node:
			extract_resources_from_node(value, resources)

# Helper function to create a UID for a resource
func create_resource_uid(resource_path: String) -> String:
	# Generate a unique identifier based on the resource path
	# You can use any logic to generate a UID, here it's just a simple hash of the path
	return str(hash(resource_path))

# Helper function to import the resource using its UID
func import_resource(resource_path: String, resource_uid: String) -> void:
	# This could involve loading the resource into the project or using the UID for further processing
	var resource = ResourceLoader.load(resource_path)
	
	if resource:
		print("Imported resource:", resource_path, "with UID:", resource_uid)
	else:
		print("Failed to import resource:", resource_path)
