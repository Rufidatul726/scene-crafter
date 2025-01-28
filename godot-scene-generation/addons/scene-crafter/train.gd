extends Button

func _on_train_button_pressed():
	print("Starting Training...")
	var url = "http://localhost:8000/train_model/"
	_start_training(url)

func _start_training(url: String) -> void:
	# Create an HTTPRequest node for making the request
	var http_request = HTTPRequest.new()
	add_child(http_request)
	
	# Connect the request_completed signal to handle the response
	http_request.connect("request_completed", Callable(self, "_on_request_completed"))
	
	# Send the POST request
	var error = http_request.request(url, [], HTTPClient.METHOD_GET)
	if error != OK:
		print("Error sending request: ", error)

func _on_request_completed(result: int, response_code: int, headers: Array, body) -> void:
	if response_code == 200:
		print("Training started successfully!")
	else:
		print("Failed to start training. Response code: ", response_code)
