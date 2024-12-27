@tool
extends Control

@onready var input= $VBoxContainer/HBoxContainer/TextEdit
@onready var sendButton= $VBoxContainer/HBoxContainer/SendButton

var apiUrl= "https://api.groq.com/openai/v1/chat/completions"
var model= "llama3-8b-8192"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	sendButton.connect("pressed", Callable(self, "_on_SubmitButton_pressed"))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_send_button_pressed() -> void:
	var text_input = input.text 
	print("User input:", text_input)
	print(OS.get_executable_path().get_base_dir())
	var version_info = Engine.get_version_info() 
	print("Godot Version: %s.%s.%s" % [version_info["major"], version_info["minor"], version_info["patch"]])
	
	var json_data = {
		"input": text_input,
		"version": version_info["major"]
	}
	
	var http := HTTPRequest.new()
	add_child(http)
	http.connect("request_completed", Callable(self, "_on_request_completed"))
	
	http.request(
		"http://127.0.0.1:8000/generate",  # Your Python server endpoint
		["Content-Type: application/json"], # Headers
		HTTPClient.METHOD_POST,
		JSON.stringify(json_data)
	)
	
func _on_request_completed(result, response_code, headers, body) -> void:
	if response_code == 200:
		var response = JSON.parse_string(body.get_string_from_utf8())
		print("Response from Python:", response)
	else:
		var response = JSON.parse_string(body.get_string_from_utf8())
		print("Error:", response_code, response)
