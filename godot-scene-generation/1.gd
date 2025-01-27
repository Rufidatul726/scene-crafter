extends Node

var speed: float = 200.0
var velocity: Vector2 = Vector2.ZERO

func _physics_process(delta: float) -> void:
	# Get input directions
	var input_x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	var input_y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")

	# Normalize input vector
	var input_vector = Vector2(input_x, input_y)
	input_vector = input_vector.normalized()

	if input_vector != Vector2.ZERO:
		velocity = input_vector * speed

	velocity = velocity.move_toward(Vector2.ZERO, speed * delta)
