#path = "D:\CS199\\bunny (2).tar\\bunny\\reconstruction\\bun_zipper.ply"

import cv2
import open3d as o3d
import trimesh
import numpy as np
import igl
from PIL import Image as im

#bin size should be multiple of mesh resolution
def spin_image(mesh, idx = 0):
    resolution = np.median(mesh.edges_unique_length)
    multiplier = 1/4
    bin_size = resolution * multiplier
    alpha_max = 0
    beta_max = 0 
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

        #print(i, j)
        a, b = bilinear_weights(alpha, beta, i, j, bin_size)
        spin_image[i, j] = spin_image[i, j] + ((1 - a)*(1 - b))
        spin_image[i + 1,j] = spin_image[i + 1, j] + ((a)*(1 - b))
        spin_image[i,j + 1] = spin_image[i,j + 1] + ((1 - a)*(b))
        spin_image[i + 1,j + 1] = spin_image[i + 1,j + 1] + ((a)*(b))
    #print(alpha_max, beta_max)
    data = spin_image.astype(np.uint8)
    pic = im.fromarray(data)
    name = "pictures/pic_{}.png".format(idx)
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


def open_spin_image(path):
    img = cv2.imread(path)
    return img

def compare_images(img1, img2, N):
    
    P = open_spin_image(img1)
    P = P.astype(np.float64).flatten()
    Q = open_spin_image(img2).astype(np.float64).flatten()
    #print(P)
    #print(Q)
    '''
    
    
    print(n1, n2)
    print(numerator)
    print(denominator)
    #print(np.corrcoef(P, Q))
    #return numerator / denominator
    
    '''

    n1 = (N * np.sum(np.multiply(P, Q))) 
    n2 = (np.sum(P) * np.sum(Q))
    numerator = n1 - n2 
    denominator = np.sqrt(((N * np.sum(np.square(P))) - np.square(np.sum(P))) * ((N * np.sum(np.square(Q))) - np.square(np.sum(Q))))
    R = np.corrcoef(P, Q)[0][1]
    
    Theta = 0 
    N_overlap = 0 
    for i in range(len(P)):
        if P[i] == Q[i]:
            N_overlap += 1
        if P[i] == 0:
            Theta+= 1

    
    print(len(P), "length of P")
    print(Theta, N_overlap)
    C = np.square(np.arctanh(R)) - (Theta * ( 1 / (N_overlap - 3)))
    
    return C

#u = pd1, v = pd2
def ridge_salience(mesh, edges, pd1, pv2):
    ridge_salience = []
    for edge in edges:
        i, j = edge
        v = mesh[i]         
        e = v - mesh[j]
        e /= np.linalg.norm(e) 
        num = pd1[i] + pd1[j] 
        num /= np.linalg.norm(num)
        k_max =  (pv2[i] + pv2[j]) / 2
        salience = np.dot(e, num) * k_max 
        ridge_salience.append(salience)
    return ridge_salience

def valley_salience(mesh, edges, pd2, pv1):
    valley_salience = [] 
    for edge in edges:
        i, j = edge
        v = mesh[i]        
        e = v - mesh[j]
        e /= np.linalg.norm(e) 
        num = pd2[i] + pd2[j] 
        num /= np.linalg.norm(num)
        k_min =  (pv1[i] + pv1[j]) / 2
        salience = np.dot(e, num) * k_min
        valley_salience.append(salience)
    return valley_salience

def curv_salience(ridge, valley):
    curv = [] 
    for i in range(len(ridge)):
        curv.append(max(ridge[i], valley[i]))
    return curv 


#edges should be (vertex idx 1, vertex idx 2, weight)
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2], reverse=True)
        #print(self.graph)
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            #print(i, e)
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)

        #print(result)
        #print(len(result), "vertices")
        self.result = result 
        #for u, v, weight in result:
            #print("%d - %d: %d" % (u, v, weight))

def set_diff2d(A, B):
    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)], 'formats':ncols * [A.dtype]}
    C = np.setdiff1d(A.copy().view(dtype), B.copy().view(dtype))
    return C

if __name__ == "__main__":
    tri_mesh = trimesh.load_mesh('mesh/Hand.obj')

    #print(np.median(tri_mesh.edges_unique_length))
    indices = [1, 20, 35, 40, 100]


    #spin_image(tri_mesh, 48001)
    #tri_mesh.show()
    resolution = np.median(tri_mesh.edges_unique_length)
    multiplier = 1/4
    bin_size = resolution * multiplier
    #print(compare_images("pictures/pic_48001.png", "pictures/pic_48001.png", bin_size))


    v = tri_mesh.vertices 
    f = tri_mesh.faces 
    e = tri_mesh.edges
    pd1, pd2, pv1, pv2 = igl.principal_curvature(v, f)

    #print(e)
    w = ridge_salience(v, e, pd1, pv2)
    
    print(len(w))
    g = Graph(len(v))
    for i in range(len(w)):
        x, y = e[i]
        g.add_edge(x, y, w[i])

    #print(len(g.graph))
    #print(g.graph[0])
    #print(g.V)
    g.kruskal_algo()
    #print(len(e))
    mst_edges = np.empty((0,2))
    mst_verts = []
    for i in g.result:
        v1, v2, w = i 
        #print(v[v1], v[v2])
        mst_verts.append([v[v1], v[v2]])
        mst_edges = np.vstack([mst_edges, np.array([i[0], i[1]])])
    
    #print(mst_edges)
        
    
    loopy_edges = np.empty((0,2))
    for i in e:
        print(i)
        if not i in mst_edges.tolist():
            loopy_edges = np.vstack([mst_edges, i])
    
    '''
    print(len(e))
    print(len(mst_edges))
    #print(len(loopy_edges))
    print(loopy_edges)
    '''
    #loopy_edges = set_diff2d(e, mst_edges)
    print(e.shape)
    print(mst_edges.shape)
    print(loopy_edges.shape)
    #p = trimesh.load_path(mst_verts)
    #print(type(p))
    #p.show()
    '''
    g = Graph(6)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 4)
    g.add_edge(1, 2, 2)
    g.add_edge(1, 0, 4)
    g.add_edge(2, 0, 4)
    g.add_edge(2, 1, 2)
    g.add_edge(2, 3, 3)
    g.add_edge(2, 5, 2)
    g.add_edge(2, 4, 4)
    g.add_edge(3, 2, 3)
    g.add_edge(3, 4, 3)
    g.add_edge(4, 2, 4)
    g.add_edge(4, 3, 3)
    g.add_edge(5, 2, 2)
    g.add_edge(5, 4, 3)
    g.kruskal_algo()
    '''
    
