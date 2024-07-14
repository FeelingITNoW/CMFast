extends Control

@onready var fd_import = $FD_Import

# Called when the node enters the scene tree for the first time.
func _ready():
	fd_import.current_dir = "/"
	#var camera = Camera3D.new()
	#camera.transform.origin = Vector3(0, 0, 10)  # Adjust position as needed
	#add_child(camera)
	
	#var light = DirectionalLight3D.new()
	#add_child(light)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_fd_import_file_selected(path):
	var mesh_instance = MeshInstance3D.new()
	var mandible_mesh = ArrayMesh.new()
	mandible_mesh = ObjParse.load_obj(path)
	if not mandible_mesh:
		print("Failed to load .obj file")
		return
	else:
		print(str(mandible_mesh))
	mesh_instance.set_mesh(mandible_mesh)
	
	print("Mesh assigned to MeshInstance3D")
	add_child(mesh_instance)
	print("MeshInstance3D added to scene")

	
