extends Camera3D

var dragging = false 
var rotating = false 
var prev_mouse_position
var next_mouse_position
var velocity
const rot_factor = .01 


func _process(delta):
	if (dragging):
		next_mouse_position = get_viewport().get_mouse_position()
		#rotate_y((next_mouse_position.x - prev_mouse_position.x) * rot_factor * delta)
		#rotate_z((next_mouse_position.y - prev_mouse_position.y) * rot_factor * delta)
		var translation_vector = Vector3(next_mouse_position.x - prev_mouse_position.x, 0, next_mouse_position.y -prev_mouse_position.y) * rot_factor
		translate(translation_vector) 
	if (rotating): 
		next_mouse_position = get_viewport().get_mouse_position()
		rotate_x((next_mouse_position.y - prev_mouse_position.y) * rot_factor * delta)
		rotate_y((next_mouse_position.x - prev_mouse_position.x) * rot_factor * delta)

func _on_recenter_camera_button_pressed():
	var position = self.position
	var rotationVector = self.rotation
	var zeroVector = Vector3(0, 0, 0)
	print('self rotation', self.rotation)
	var oppositeTranslationVector = Vector3(-1 * self.position.x, -1 * self.position.y, -1 * self.position.z)
	var oppositeRotationVector = Vector3(-1 * rotationVector).normalized() 
	self.translate(oppositeTranslationVector)
	self.set_rotation(zeroVector)
	
func _on_drag_camera_button_button_up():
	dragging = false

func _on_drag_camera_button_button_down():
	dragging = true
	prev_mouse_position = get_viewport().get_mouse_position()	

func _on_rotate_camera_button_button_down():
	rotating = true 
	prev_mouse_position = get_viewport().get_mouse_position()

func _on_rotate_camera_button_button_up():
	rotating = false
