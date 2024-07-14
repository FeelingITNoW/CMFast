@tool
extends EditorPlugin


func _enter_tree():
	add_custom_type("Fracture Mesh", "Node3D", preload("fractureMeshObject.gd"), preload('res://icon.svg'))
	


func _exit_tree():
	# Clean-up of the plugin goes here.
	pass
