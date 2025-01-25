@tool
extends EditorPlugin

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.connect("request_completed", Callable(self, "_on_request_completed"))
	
	http.request(
		"http://127.0.0.1:8000/getdir/",
		[], # Headers
		HTTPClient.METHOD_GET
	)

func _on_request_completed(result, response_code, headers, body) -> void:
	var response = JSON.parse_string(body.get_string_from_utf8())
	if response_code == 200:
		print("Response from Python:", response)
	else:
		print("Error:", response_code, response)
