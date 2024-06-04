extends Camera3D

var rotating = false 
var prev_mouse_position
var next_mouse_position
var velocity
const rot_factor = .01 


func _process(delta):
	if (rotating):
		next_mouse_position = get_viewport().get_mouse_position()
		#rotate_y((next_mouse_position.x - prev_mouse_position.x) * rot_factor * delta)
		#rotate_z((next_mouse_position.y - prev_mouse_position.y) * rot_factor * delta)
		var translation_vector = Vector3(next_mouse_position.x - prev_mouse_position.x, 0, next_mouse_position.y -prev_mouse_position.y) * rot_factor
		translate(translation_vector) 
	
func _on_recenter_camera_button_pressed():
	var position = self.position
	var rotation = self.rotation
	var oppositeVector = Vector3(-1 * self.position.x, -1 * self.position.y, -1 * self.position.z)
	self.translate(oppositeVector)

func _on_drag_camera_button_button_up():
	rotating = false
	
func _on_drag_camera_button_button_down():
	rotating = true
	prev_mouse_position = get_viewport().get_mouse_position()
