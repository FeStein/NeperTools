#-------------------------------------------------------------------
#Nucleation Model to create initial points for FEAP Input Skript 
#Mesh + TessFile needes as Input 
#-------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random 
import json
#General Definitions
class Nucleuspoint_2D():
    
    def __init__(self,x,y,mvariant):
        self.x = x
        self.y = y
        self.mvariant = mvariant
        self.nodes = []
        
    def _inside_circle(self,node,radius):
        return (node.x - self.x)**2 + (node.y - self.y)**2 < radius**2 
        
    def fetch_nodes(self,node_list,radius):
        for node in node_list:
            if self._inside_circle(node,radius):
                self.nodes.append(node)

class Nucleuspoint_3D():
    
    def __init__(self,x,y,z,mvariant):
        self.x = x
        self.y = y
        self.z = z
        self.mvariant = mvariant
        self.nodes = []
        
    def _inside_sphere(self,node,radius):
        return (node.x - self.x)**2 + (node.y - self.y)**2 + (node.z - self.z)**2 < radius**2 
        
    def fetch_nodes(self,list_of_nodes,radius):
        for node in list_of_nodes:
            if self._inside_sphere(node,radius):
                self.nodes.append(node)
#--------------------------------------------------------------------
#2D Version
#--------------------------------------------------------------------

class Grain():
    
    def __init__(self,matn,elems,mesh,tf):
        self.matn = matn
        self.elems = elems
        self.mesh = mesh
        self.tf = tf
        self.node_list = []
        self.boundary_node_list = []
        self.triple_node_list = []
        self.node_id_set = set()
        self._get_node_id_set()
        self.node_grid_x = None
        self.node_grid_y = None
        self.vertex_point_list = [] #list of vertex tuples (x_cord,y_cord)
        self._get_vertex_point_list()
        
    def fetch_nodes(self):
        '''Fetches nodes for the three different node lists (all,triple,boundary)'''
        self._get_nodes()
        self._get_triple_node_list()
        self._get_node_grid()
        self._get_boundary_nodes()
        
        
    def _get_node_id_set(self):
        '''Calculates set of node ids contained by the grain'''
        for elem in self.mesh.elems:
            if self.matn == elem.matn:
                for node_id in elem.nodes:
                    self.node_id_set.add(node_id)
                    
    def _getcords(self,id):
        '''gets cords for a given vertex id'''
        for vert in self.tf.vertex_list:
            if vert.id == id:
                return [vert.x,vert.y]
                    
    def _get_nodes(self):
        '''gets all nodes contained by the grain, using the node id set'''
        for node in self.mesh.nodes:
            if node.id in self.node_id_set:
                self.node_list.append(node)
        
    def _get_vertex_point_list(self):
        '''gets vetex point list, by comparison of grain.matn to face.id (should be identical)'''
        face = next(face for face in self.tf.face_list if face.id == self.matn)
        self.vertex_point_list = [self._getcords(vert) for vert in face.vertex_list]
    
    def _get_triple_node_list(self):
        '''fetches all triple nodes contained by the grain (triple node -> closest distance to numerical triple point)'''
        for [px,py] in self.vertex_point_list:
            tmp_triple_node = self.node_list[0]
            tmp_distance = np.sqrt((px - tmp_triple_node.x)**2 + (py - tmp_triple_node.y)**2)            
            for node in self.node_list:
                distance = np.sqrt((px - node.x)**2 + (py - node.y)**2) 
                if distance < tmp_distance:
                    tmp_triple_node = node
                    tmp_distance = distance
            self.triple_node_list.append(tmp_triple_node)                
    
    def _get_node_grid(self):
        '''creates a grid of all nodes inside a grain -> later used to calculate the boundary grains'''
        #find all diff y-values of nodes
        node_grid = []
        y_values = sorted(list(set([node.y for node in self.node_list])))
        x_values = sorted(list(set([node.x for node in self.node_list])))
        
        for x_val in x_values:
            sublist = sorted([node for node in self.node_list if node.x == x_val],key= lambda node: node.y)
            node_grid.append(sublist)
        
        self.node_grid_x = node_grid
        
        for y_val in y_values:
            sublist = sorted([node for node in self.node_list if node.y == y_val],key= lambda node: node.x)
            node_grid.append(sublist)
        
        self.node_grid_y = node_grid

    def _get_boundary_nodes(self):
        '''get boundary nodes at the grain (node with less than 4 neighbours)'''
        for x_index in range(len(self.node_grid_x)):
            for y_index in range(len(self.node_grid_x[x_index])):
                if x_index - 1 < 0 or y_index - 1 < 0:
                    self.boundary_node_list.append(self.node_grid_x[x_index][y_index])
                    continue
                if x_index + 1 >= len(self.node_grid_x) or y_index + 1 >= len(self.node_grid_x[x_index]):
                    self.boundary_node_list.append(self.node_grid_x[x_index][y_index])
                    continue
        
        for y_index in range(len(self.node_grid_y)):
            for x_index in range(len(self.node_grid_y[y_index])):
                if x_index - 1 < 0 or y_index - 1 < 0:
                    self.boundary_node_list.append(self.node_grid_y[y_index][x_index])        
        
        
    def visu(self):
        '''visualisation of the grain'''
        fig,ax = plt.subplots(figsize=(7,7))
        for c,edge in enumerate(self.tf.edge_list):
            x = self._getcords(edge.v1)
            y = self._getcords(edge.v2)
            tg = list(zip(x,y))
            plt.plot(tg[0],tg[1], 'k')
            ax.annotate(str(c), ((sum(tg[0]))/2, (sum(tg[1]))/2))
            
        #plot whole mesh
        x_values = [node.x for node in self.node_list]
        y_values = [node.y for node in self.node_list]
        plt.plot(x_values,y_values,'.',c='g',ms=1)
        #plot grain boundarys nodes
        x_values = [node.x for node in self.boundary_node_list]
        y_values = [node.y for node in self.boundary_node_list]
        plt.plot(x_values,y_values,'.',c='b',markersize=2)
        
        #plot grain boundarys nodes
        x_values = [node.x for node in self.triple_node_list]
        y_values = [node.y for node in self.triple_node_list]
        plt.plot(x_values,y_values,'.',c='r',ms=5)
        
        plt.xlim(-0.02,1.02)                                                                                                                                                                        
        plt.ylim(-0.02,1.02)
        plt.show()


class NucleusModel2D():
    
    def __init__(self,config_filename,mesh,tf):
        with open(config_filename) as config_file:
            cf = json.load(config_file) 
        self.cf = cf
        self.mat_variants = self.cf['general']['mat_variants']
        self.mesh = mesh
        self.tf = tf
        
        self.np_list = []    
        self.removed_nodes = []  #contains all nodes which are removed e.g. nodes wich are used to lock boundaries 
        
        self.grain_list = [Grain(es.setMat,es.elems,mesh,tf) for es in self.mesh.elsets]
        self._rem_duplicates_list()

        for grain in self.grain_list: grain.fetch_nodes()

    def _rem_duplicates_list(self):
        '''checks all node ids per grain in  the grain list, then removes both instances of duplicates of ids
        contained in more than one grain. This makes sure that nodes, which are contained in elements of different
        grains are filterd out. Needs to be done before all nodes are fetched (fetching is based on node id list).
        -------------------------------------------------
        All removed nodes are collected in removed_nodes_id_set and then used to fetch the removed nodes. this is 
        useful to later lock the boundaries of grains
        '''
        removed_nodes_id_set = set()
        remove_sets = [grain.node_id_set for grain in self.grain_list]
        for i,grain in enumerate(self.grain_list):
            for j,rem_set in enumerate(remove_sets):
                if i == j: continue
                removed_nodes_id_set = removed_nodes_id_set | set.intersection(grain.node_id_set, rem_set)
                grain.node_id_set = grain.node_id_set - rem_set
        #collect removed nodes 
        if self.cf['nmodel']['lock_bound']:
            for node in self.mesh.nodes:
                if node.id in removed_nodes_id_set:
                    self.removed_nodes.append(node)
                
    def create_model(self):
        radius = self.cf['nmodel']['radius'] 
        quantity = self.cf['nmodel']['quantity']
        grain_prob = self.cf['nmodel']['grain_prob']
        bound_prob = self.cf['nmodel']['bound_prob']
        triple_prob = self.cf['nmodel']['triple_prob']
        if grain_prob + bound_prob + triple_prob != 1:
            sum_prob = grain_prob + bound_prob + triple_prob
            grain_prob = grain_prob / sum_prob
            bound_prob = bound_prob / sum_prob
            triple_prob = triple_prob / sum_prob
        total_nodes = sum([len(grain.node_list) for grain in self.grain_list])
        total_triple = sum([len(grain.triple_node_list) for grain in self.grain_list])
        if triple_prob == True:
            #überall hinsetzten, rest aufteilen
            quantity_triple = total_triple
            quantity = quantity - quantity_triple 
            if quantity > 0:
                quantity_grain = int(grain_prob*quantity)
                quantity_bound = int(bound_prob*quantity)
            else:
                quantity_grain = 0
                quantity_bound = 0
            all_triple = True
            
        else:
            all_triple = False
            #Split to different areas
            quantity_grain = int(grain_prob*quantity)
            overlab = grain_prob*quantity - int(grain_prob*quantity)

            quantity_triple = int(triple_prob*quantity + overlab)
            overlab  = triple_prob*quantity + overlab - quantity_triple

            quantity_bound = quantity - quantity_grain - quantity_triple
            #Check if sum is still fine
            if quantity_triple > total_triple:
                quantity_bound += quantity_triple - total_triple
        
        #Here the NP's are created:
        overlab_g = 0
        overlab_b = 0
        overlab_t = 0
        for grain in self.grain_list:
            mv = 1
            #Grain Nodes:
            num_points = int((len(grain.node_list)/total_nodes)*quantity_grain + overlab_g)
            overlab_g = (len(grain.node_list)/total_nodes)*quantity_grain + overlab_g - num_points
            point_index = np.random.randint(len(grain.node_list), size=num_points)
            point_index = sorted(list(point_index))
            for i in point_index:
                if mv == 1:
                    mv = 2
                else: 
                    mv = 1
                n= grain.node_list[i]
                NP = Nucleuspoint_2D(n.x,n.y,mv)
                NP.fetch_nodes(grain.node_list,radius)
                self.np_list.append(NP)
            #Boundary Nodes:
            num_points = int((len(grain.node_list)/total_nodes)*quantity_bound + overlab_b)
            overlab_b = (len(grain.node_list)/total_nodes)*quantity_bound + overlab_b - num_points
            point_index = np.random.randint(len(grain.boundary_node_list), size=num_points)
            point_index = sorted(list(point_index))
            for i in point_index:
                if mv == 1:
                    mv = 2
                else: 
                    mv = 1
                n= grain.boundary_node_list[i]
                NP = Nucleuspoint_2D(n.x,n.y,mv)
                NP.fetch_nodes(grain.node_list,radius)
                self.np_list.append(NP)
            #Triple Nodes:
            if all_triple:
                for node in grain.triple_node_list:
                    #mv = int(np.random.random()*martvariants) + 1
                    if mv == 1:
                        mv = 2
                    else: 
                        mv = 1

                    NP = Nucleuspoint_2D(node.x,node.y,mv)
                    NP.fetch_nodes(grain.node_list,radius)
                    self.np_list.append(NP)
            else:
                num_points = int((len(grain.node_list)/total_nodes)*quantity_triple + overlab_t)
                overlab_t = (len(grain.node_list)/total_nodes)*quantity_triple + overlab_t - num_points
                point_index = np.random.randint(len(grain.triple_node_list), size=num_points)
                point_index = sorted(list(point_index))
                for i in point_index:
                    if mv == 1:
                        mv = 2
                    else: 
                        mv = 1
                    n= grain.triple_node_list[i]
                    NP = Nucleuspoint_2D(n.x,n.y,mv)
                    NP.fetch_nodes(grain.node_list,radius)
                    self.np_list.append(NP)            
        
    def _getcords(self,id):
        for vert in self.tf.vertex_list:
            if vert.id == id:
                return [vert.x,vert.y]
            
    def visualize_model(self,path = None):
        #Printing of Structure
        fig,ax = plt.subplots(figsize=(10,10))
        for edge in self.tf.edge_list:
            x = self._getcords(edge.v1)
            y = self._getcords(edge.v2)
            tg = list(zip(x,y))
            plt.plot(tg[0],tg[1], 'k')
            
        #Printing of np.points 
        for np in self.np_list:
            x_values = [node.x for node in np.nodes]
            y_values = [node.y for node in np.nodes]
            plt.plot(x_values,y_values,'.',c = 'g' if np.mvariant == 1 else 'b',ms = 2)
        plt.ylim(-0.01,1.01)
        plt.xlim(-0.01,1.01)
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        if path != None: plt.savefig(path)
        
        plt.show()

#--------------------------------------------------------------------
#3D Version
#--------------------------------------------------------------------

class Grain3D():
    
    def __init__(self,matn,elems,mesh,tf):
        self.matn = matn
        self.elems = elems
        self.mesh = mesh
        self.tf = tf
        self.edge_list = []
        self.node_list = []
        
        self.boundary_node_list = []
        self.triple_node_list = []
        self.node_id_set = set()
        
        self.boundary_id_set = set()
        self.triple_id_set = set()
        
        self._get_node_id_set()
        
        self._get_nodes()
        
    def fetch_nodes(self):
        self._get_nodes()
    
    def _get_node_id_set(self):
        '''Calculates set of node ids contained by the grain'''
        for elem in self.mesh.elems:
            if self.matn == elem.matn:
                for node_id in elem.nodes:
                    self.node_id_set.add(node_id)
                    
    def _get_nodes(self):
        '''gets all nodes contained by the grain, using the node id set'''
        for node in self.mesh.nodes:
            if node.id in self.node_id_set:
                self.node_list.append(node)
                
    def fetch_node_categories(self):
        
        def points_in_cylinder(pt1, pt2, r, q):
            pt1,pt2 = np.array(pt1),np.array(pt2)
            vec = pt2-pt1
            const = r * np.linalg.norm(vec)
            return np.dot(q - pt1, vec) >= 0 and np.dot(q - pt2, vec) <= 0 and np.linalg.norm(np.cross(q - pt1, vec)) <= const
        
        def getcords(id):
            '''gets cords for a given vertex id'''
            for vert in self.tf.vertex_list:
                if vert.id == id:
                    return [vert.x,vert.y,vert.z]
        
        #get unique coordinate values of each grain should be <= element count per side
        x_set = set([node.x for node in self.node_list])
        y_set = set([node.y for node in self.node_list])
        z_set = set([node.z for node in self.node_list])
        
        #calculate a sorted list 
        x_list = sorted(list(x_set))
        y_list = sorted(list(y_set))
        z_list = sorted(list(z_set))
        
        node_grid = []
        
        for x_val in x_list:
            tmp_node_list = [node for node in self.node_list if node.x == x_val]
            #xy-plane
            for y_val in y_list:
                sublist = sorted([node for node in tmp_node_list if node.y == y_val],key = lambda node: node.z)
                if len(sublist) > 1:
                    self.boundary_node_list.append(sublist[0])
                    self.boundary_node_list.append(sublist[-1])
                elif len(sublist) == 1:
                    self.boundary_node_list.append(sublist[0])
            #xz-plane
            for z_val in z_list:
                sublist = sorted([node for node in tmp_node_list if node.z == z_val],key = lambda node: node.y)
                if len(sublist) > 1:
                    self.boundary_node_list.append(sublist[0])
                    self.boundary_node_list.append(sublist[-1])
                elif len(sublist) == 1:
                    self.boundary_node_list.append(sublist[0])
        
        #detection of triple points
        #Get edges of polyhedron/grain
        edge_id_set = set() #-> contains all edges of grain
        #Select Polyhedrona according to grain id
        for polyhedron in self.tf.polyhedron_list:
            if polyhedron.id == self.matn:
                break
        
        for face_id in polyhedron.face_id_list:
            for face in self.tf.face_list:
                if face.id == face_id:
                    for edge in self.tf.edge_list:
                        edge_id_set.add(edge.id)

        #init edges to ids                
        for edge in self.tf.edge_list:
            if edge.id in edge_id_set:
                self.edge_list.append(edge)
            
        print('Edges of Polyhedron ' + str(self.matn) + ' initialized')
        
        #yz-plane
        for y_val in y_list:
            tmp_node_list = [node for node in self.node_list if node.y == y_val]
            for z_val in z_list:
                sublist = sorted([node for node in tmp_node_list if node.z == z_val], key = lambda node: node.x)
                if len(sublist) > 1:
                    self.boundary_node_list.append(sublist[0])
                    self.boundary_node_list.append(sublist[-1])
                elif len(sublist) == 1:
                    self.boundary_node_list.append(sublist[0])
    
        #rem duplicates in boundary node list
        self.boundary_node_list = list(set(self.boundary_node_list))
        
        rad = 0.02 #tbd should be dependend on mesh
        for node in self.boundary_node_list:
            for edge in self.edge_list:
                p1,p2 = getcords(edge.v1),getcords(edge.v2)
                if points_in_cylinder(p1,p2,rad,[node.x,node.y,node.z]):
                    self.triple_node_list.append(node)
        #rem duplicates in triple node list
        self.triple_node_list = list(set(self.triple_node_list))

class NucleusModel3D():
    
    def __init__(self,config_filename,mesh,tf):
        with open(config_filename) as config_file:
            cf = json.load(config_file) 
        self.cf = cf
        self.mat_variants = cf['general']['mat_variants']

        self.mesh = mesh
        self.tf = tf
        
        self.np_list = []
        self.dup_node_list = [] #useful for visualization of deleted nodes 
        self.bound_node_list = []
        
        self.grain_list = [Grain3D(es.setMat,es.elems,mesh,tf) for es in self.mesh.elsets] #tbd
        self._rem_duplicates_list()
        
        for grain in self.grain_list:
            grain.fetch_nodes()
            grain.fetch_node_categories()

    def _rem_duplicates_list(self):
        '''checks all node ids per grain in  the grain list, then removes both instances of duplicates of ids
        contained in more than one grain. This makes sure that nodes, which are contained in elements of different
        grains are filterd out. Needs to be done before all nodes are fetched (fetching is based on node id list).'''
        remove_sets = [grain.node_id_set for grain in self.grain_list]
        dup_set = set()
        for i,grain in enumerate(self.grain_list):
            for j,rem_set in enumerate(remove_sets):
                if i == j: continue
                current_duplicates = grain.node_id_set.intersection(rem_set)
                current_triples = current_duplicates.intersection(grain.boundary_id_set)
                grain.triple_id_set.update(current_triples)
                grain.boundary_id_set.update(current_duplicates)
                dup_set.update(current_duplicates)
                grain.node_id_set = grain.node_id_set - rem_set
                
                
        print('removed dup nodes')
        #Calculated duplicated Nodes
        for node in self.mesh.nodes:
            if node.id in dup_set:
                self.dup_node_list.append(node)
        print('calculated dup nodes')
    
    def getcords(self,id):
        for vert in self.tf.vertex_list:
            if vert.id == id:
                return [vert.x,vert.y,vert.z]
        
    def create_model(self):
        radius = self.cf['nmodel']['radius']
        quantity = self.cf['nmodel']['quantity']
        grain_prob = self.cf['nmodel']['grain_prob']
        bound_prob = self.cf['nmodel']['bound_prob']
        triple_prob = self.cf['nmodel']['triple_prob']
        martvariants = self.cf['general']['mat_variants']
        self.np_list = []
        total_nodes = sum([len(grain.node_list) for grain in self.grain_list])
        total_triple = sum([len(grain.triple_node_list) for grain in self.grain_list])
        
        for grain in self.grain_list:
            print('Grain ' + str(grain.matn))
            mv = 1
            num_points = round((len(grain.node_list)/total_nodes)*quantity)
            #inside grain
            if len(grain.node_list) > 0:
                point_index = np.random.randint(len(grain.node_list), size=round(num_points*grain_prob))
            else: 
                point_index = []
            point_index = sorted(list(point_index))
            for i in point_index:
                if mv < martvariants:
                    mv += 1
                else: 
                    mv = 1
                n= grain.node_list[i]
                NP = Nucleuspoint_3D(n.x,n.y,n.z,mv)
                NP.fetch_nodes(grain.node_list,radius)
                self.np_list.append(NP)
                
            #boundary faces
            if len(grain.boundary_node_list) > 0:
                point_index = np.random.randint(len(grain.boundary_node_list), size=int(num_points*bound_prob))
            else: 
                point_index = []
            point_index = sorted(list(point_index))
            for i in point_index:
                if mv < martvariants:
                    mv += 1
                else: 
                    mv = 1
                n= grain.boundary_node_list[i]
                NP = Nucleuspoint_3D(n.x,n.y,n.z,mv)
                NP.fetch_nodes(grain.node_list,radius)
                self.np_list.append(NP)
                
            #triple lines 
            if len(grain.triple_node_list) > 0:
                point_index = np.random.randint(len(grain.triple_node_list), size=round(num_points*triple_prob))
            else: 
                point_index = []
            point_index = sorted(list(point_index))
            for i in point_index:
                if mv < martvariants:
                    mv += 1
                else: 
                    mv = 1
                n= grain.triple_node_list[i]
                NP = Nucleuspoint_3D(n.x,n.y,n.z,mv)
                NP.fetch_nodes(grain.node_list,radius)
                self.np_list.append(NP)
                
    def remove_duplicate_np_list(self):
        node_test_set = set()
        for NP in self.np_list:
            non_dup_nodes = [node for node in NP.nodes if node not in node_test_set]
            NP.nodes = non_dup_nodes
            node_test_set.update(non_dup_nodes)

    def visualize_model(self,path = None):
        fig = plt.figure(figsize=(7,7))
        ax = plt.axes(projection="3d")

        #Printing of Structure
        def tgetcords(id):
            for vert in self.tf.vertex_list:
                if vert.id == id:
                    return [vert.x,vert.y,vert.z]

        for edge in self.tf.edge_list:
            x = tgetcords(edge.v1)
            y = tgetcords(edge.v2)
            tg = list(zip(x,y))
            plt.plot(tg[0],tg[1],tg[2], 'k')
        
        #plot NukleusPoints
        colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan','b','g']
        for mtv in range(self.mat_variants):
            x_values = []
            y_values = []
            z_values = []
            NP_fix = [np for np in self.np_list if np.mvariant == mtv + 1]
            for NP in NP_fix:
                
                x_values.extend([node.x for node in NP.nodes])
                y_values.extend([node.y for node in NP.nodes])
                z_values.extend([node.z for node in NP.nodes])

                ax.plot(x_values,y_values,z_values,'.',c=colors[mtv ],alpha = 0.5)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0,0)
        if path != None:
            plt.savefig(path)
        plt.show()
