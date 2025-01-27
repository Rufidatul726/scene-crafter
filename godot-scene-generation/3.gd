extends Node

var speed: float = 200.0
var velocity: Vector2 = Vector2.ZERO

func _physics_process(delta: float) -> void:
	# Get input directions
	if Input.is_action_pressed("ui_right"):
		velocity.x += 1
	if Input.is_action_pressed("ui_left"):
		velocity.x -= 1
	if Input.is_action_pressed("ui_down"):
		velocity.y += 1
	if Input.is_action_pressed("ui_up"):
		velocity.y -= 1

	# Normalize the velocity vector
	velocity = velocity.normalized()

	# Limit the speed
	velocity *= speed
