@tool
extends EditorPlugin

var log_file

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.connect("request_completed", Callable(self, "_on_request_completed"))
	
	http.request(
		"http://127.0.0.1:8000/getdir/",  # Your Python server endpoint
		["Content-Type: application/json"], # Headers
		HTTPClient.METHOD_GET
	)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
