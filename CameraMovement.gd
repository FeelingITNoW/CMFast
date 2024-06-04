extends Camera3D

var rotating = false 
var prev_mouse_position
var next_mouse_position
var velocity
const rot_factor = .01 

# Called when the node enters the scene tree for the first time.
func _process(delta):
	
	if (Input.is_action_just_pressed(("ui_mouse_click"))): 
		rotating = true 
		prev_mouse_position = get_viewport().get_mouse_position();
	
	if (Input.is_action_just_released(('ui_mouse_click'))):
		rotating = false 
		next_mouse_position = get_viewport().get_mouse_position()
	
	if (rotating):
		next_mouse_position = get_viewport().get_mouse_position()
		#rotate_y((next_mouse_position.x - prev_mouse_position.x) * rot_factor * delta)
		#rotate_z((next_mouse_position.y - prev_mouse_position.y) * rot_factor * delta)
		var translation_vector = Vector3(next_mouse_position.x - prev_mouse_position.x, 0, next_mouse_position.y -prev_mouse_position.y) * rot_factor
		translate(translation_vector) 
	




func _on_button_pressed():
	print('pre button press', self.position)
	var position = self.position
	var rotation = self.rotation
	print('rotation', rotation)
	var oppositeVector = Vector3(-1 * self.position.x, -1 * self.position.y, -1 * self.position.z)
	self.translate(oppositeVector)
	print('post button press', self.position)
