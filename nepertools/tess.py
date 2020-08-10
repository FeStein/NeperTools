#-------------------------------------------------------------------
#Definitions regarding .tess Files, as well as the Implementation
#of the .tess Parser
#-------------------------------------------------------------------
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

class TessFile:
    """
    Tess File class, containing the different elementes of a .tess file in 
    lists of subclasses.

    Attributes
    -----------
    cell: int 
        -> number of cells contained in the .tess file 

    dimensions: int

    edge_list: list of Edge

    vertex_list: list of Vertex

    face_list: list of Face

    seed_list: list of Seed

    polyhedron_list: list of Polyhedron

    orientation_list: list of orientations -> orientation are lists as well
        orientation: [phi1,phi2,phi3] (float) in degree
    """
    def __init__(self):
        """
        Initializes a new tess_file, setting all content lists empty
        """
        self.cell = 0
        self.dimensions = 0
        self.edge_list = []
        self.vertex_list = []
        self.face_list = []
        self.seed_list = []
        self.polyhedron_list = []
        self.orientation_list = []

    def visu(self):
        """
        Prints a visualization of the given structure using matplotlib.
        -Grain boundaries are marked black
        -Seeds are marked red
        """
        def getcords(id):
            '''
            Get the coordinates (x,y)/(x,y,z) for a given vertex id
            '''
            for vert in self.vertex_list:
                if vert.id == id:
                    if self.dimensions == 2:
                        return [vert.x,vert.y] 
                    else:
                        return [vert.x,vert.y,vert.z]

        if self.dimensions == 2:
            _,ax = plt.subplots(figsize=(10,10))
            for edge in self.edge_list:
                x = getcords(edge.v1)
                y = getcords(edge.v2)
                tg = list(zip(x,y))
                plt.plot(tg[0],tg[1], 'k')

            for seed in self.seed_list:
                plt.plot(seed.x,seed.y,'.',c='r',ms=8)

            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                        hspace = 0, wspace = 0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

            plt.xlim(-0.01,1.01)
            plt.ylim(-0.01,1.01)
            plt.show()
        elif self.dimensions == 3:
            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection="3d")

            for edge in self.edge_list:
                x = getcords(edge.v1)
                y = getcords(edge.v2)
                tg = list(zip(x,y))
                plt.plot(tg[0],tg[1],tg[2], 'k')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

            plt.show()
        else:
            print('Dimensions must be 2D or 3D, most likely something went wrong while parsing')

class Vertex:
    """
    Attributes
    -----------
    id: int
    x: float
    y: float
    z: float (=0 for 2D Structures)
    """
    def __init__(self,id,x,y,z):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

class Edge:
    """
    Attributes
    -----------
    id: int
    v1: int
    v2: int
    v3: int
    """

    def __init__(self,id,vertex1,vertex2,vertex3):
        self.id = int(id)
        self.v1 = int(vertex1)
        self.v2 = int(vertex2)
        self.v3 = int(vertex3)

class Face:
    """
    Attributes
    -----------
    id: int
    vertex_list: list of int
    edge_list: list of int
    """

    def __init__(self,id):
        self.id = int(id)
        self.vertex_list = []
        self.edge_list = []

class Seed:
    """
    Attributes
    -----------
    id: int
    x: float
    y: float
    z: float
    weight: float
    """
    def __init__(self,*args):
        self.id = int(args[0])
        self.x = float(args[1])
        self.y = float(args[2])
        self.z = float(args[3])
        self.weight = float(args[4])

class Polyhedron:
    """
    Attributes
    -----------
    id: int
    number_of_faces: int
    face_id_list: list of int
    """

    def __init__(self,id,nf,face_id_list):
        self.id = int(id)
        self.number_of_faces = int(nf)
        self.face_id_list = [int(face) for face in face_id_list]

class TESS_Parser:
    '''
    Parser, used to parse .tess files
    '''

    READ_CELL = 1
    READ_VERTEX = 2
    READ_EDGE = 3
    READ_FACE = 4
    READ_SEEDS = 5
    READ_POLYHEDRON = 6
    READ_ORI = 7
    READ_GENERAL = 8
    UNKNOWN = 0
    
    def __init__(self,filename):
        '''
        Init method to specify filename/path which will be parsed

        Keyword arguments:
        -----------------------
        filename - path to file
        '''
        self.filename = filename

    def parse(self):
        face_lines = []
        tess_file = TessFile()
        readmode = TESS_Parser.UNKNOWN
        with open(self.filename, 'r') as f:
            for _, line in tqdm(enumerate(f.readlines())):
                #Checking for keywords -> choose parsing modes
                if line.strip().startswith("*"):
                    if (line.strip().split(',')[0]) == "**cell":
                        readmode = TESS_Parser.READ_CELL
                        continue

                    if (line.strip().split(',')[0]) == "**general":
                        readmode = TESS_Parser.READ_GENERAL
                        continue
                        
                    elif (line.strip().split(',')[0]) == "**vertex":
                        readmode = TESS_Parser.READ_VERTEX
                        continue
                        
                    elif (line.strip().split(',')[0]) == "**edge":
                        readmode = TESS_Parser.READ_EDGE
                        continue
                        
                    elif (line.strip().split(',')[0]) == "**face":
                        readmode = TESS_Parser.READ_FACE
                        continue
                        
                    elif (line.strip().split(',')[0]) == "*seed":   
                        readmode = TESS_Parser.READ_SEEDS
                        continue

                    elif (line.strip().split(',')[0]) == "**polyhedron": 
                        readmode = TESS_Parser.READ_POLYHEDRON
                        continue
                    
                    elif (line.strip().split(',')[0]) == "*ori": 
                        readmode = TESS_Parser.READ_ORI
                        continue

                    else:
                        readmode = TESS_Parser.UNKNOWN
                        continue
                        
                elif line.strip() == "":
                    continue
                    
                else:
                    #Parse general
                    if readmode == TESS_Parser.READ_GENERAL:
                        splitted = line.split()
                        if len(splitted) == 2:
                            tess_file.dimensions = int(splitted[0])
                    #Parse cell
                    if readmode == TESS_Parser.READ_CELL:
                        tess_file.cell = int(line.strip())
                        
                    #Parse vertex
                    if readmode == TESS_Parser.READ_VERTEX:
                        splitted = line.split()
                        if len(splitted) == 5:
                            nvertex = Vertex(*splitted[:-1])
                            tess_file.vertex_list.append(nvertex)
                    #Parse edge
                    if readmode == TESS_Parser.READ_EDGE:
                        splitted = line.split()
                        if len(splitted) == 4:
                            nedge  = Edge(*splitted)
                            tess_file.edge_list.append(nedge)
                    
                    #Parse face
                    if readmode == TESS_Parser.READ_FACE:
                        face_lines.append(line)   

                    #Parse Seed
                    if readmode == TESS_Parser.READ_SEEDS:
                        splitted = line.split()
                        see = Seed(*splitted)
                        tess_file.seed_list.append(see)

                    #Parse Polyhedron
                    if readmode == TESS_Parser.READ_POLYHEDRON:
                        splitted = line.split()
                        if len(splitted) > 2:
                            polyh = Polyhedron(splitted[0],splitted[1],splitted[2:])
                            tess_file.polyhedron_list.append(polyh)

                    #Parse Orientations
                    if readmode == TESS_Parser.READ_ORI:
                        oris = re.findall(r'-?[0-9]+\.[0-9]+',line)
                        if len(oris)== 3:
                            oris = [float(o) for o in oris]
                            tess_file.orientation_list.append(oris)
                
                    #UNKNNOWN
                    elif readmode == TESS_Parser.UNKNOWN:
                        continue #do nothing
                        
        #create faces:
        for counter,line in enumerate(face_lines):
            if counter%4 == 1:
                splitted = line.split()
                tmp_face = Face(splitted[0])
                tmp_face.vertex_list = list(map(int,splitted[2:]))
            elif counter%4 == 2:
                splitted = line.split()
                tmp_face.edge_list = list(map(int,splitted[1:]))
                tess_file.face_list.append(tmp_face)
        
        print('Parsed Tess File')
        return tess_file