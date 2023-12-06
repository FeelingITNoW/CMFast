path = "D:\CS199\\bunny (2).tar\\bunny\\reconstruction\\bun_zipper.ply"


import open3d as o3d
import trimesh
import numpy as np
from PIL import Image as im
#bin size should be multiple of mesh resolution
def spin_image(mesh, idx = 0):
    resolution = np.median(tri_mesh.edges_unique_length)
    multiplier = 1/4
    alpha_max = 0
    beta_max = 0 
    bin_size = resolution * multiplier
    image_width = 40
    spin_image = np.empty((2000, 2000))
    #num_verts = len(mesh.vertices)

    #for i in range(num_verts):
    p, n = generate_oriented_point(idx, mesh)
    
    for x in mesh.vertices:
        alpha = np.sqrt(np.square(np.linalg.norm(x - p)) - (np.dot(n, (np.square(x - p)))))
        beta = np.dot(n, (x - p))
        alpha_max = max(alpha_max, alpha)
        beta_max = max(beta_max, beta)
        #print(alpha, beta)
        i, j = spin_image_bins(alpha, beta, bin_size, image_width)

        print(i, j)
        a, b = bilinear_weights(alpha, beta, i, j, bin_size)
        spin_image[i, j] = spin_image[i, j] + ((1 - a)*(1 - b))
        spin_image[i + 1,j] = spin_image[i + 1, j] + ((a)*(1 - b))
        spin_image[i,j + 1] = spin_image[i,j + 1] + ((1 - a)*(b))
        spin_image[i + 1,j + 1] = spin_image[i + 1,j + 1] + ((a)*(b))
    #print(alpha_max, beta_max)
    data = spin_image.astype(np.uint8)
    pic = im.fromarray(data)
    name = "pic_{}.png".format(idx)
    pic.save(name)


def spin_image_bins(alpha, beta, bin_size, image_width):
    i = int(np.floor(((image_width / 2 ) - beta) / bin_size ))
    j = int(np.floor(alpha / bin_size))

    return i, j


def bilinear_weights(alpha, beta, i, j, bin_size):
    a = alpha - (i * bin_size)
    b = beta - (j * bin_size)

    return a, b 


def generate_oriented_point(vert_index, mesh):
    #Will assume that trimesh indexes vertices with their respective normals consistently.
    p = mesh.vertices[vert_index]
    n = mesh.vertex_normals[vert_index]
    return p, n

tri_mesh = trimesh.load_mesh('Hand.obj')

print(np.median(tri_mesh.edges_unique_length))
indices = [1, 20, 35, 40, 100]


spin_image(tri_mesh, 10000)
#tri_mesh.show()
