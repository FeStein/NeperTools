#-------------------------------------------------------------------
#Definitions regarding .inp Files, as well as the Implementation
#of the .inp Parser -> Output: Mesh Object 
#-------------------------------------------------------------------
import re
import matplotlib.pyplot as plt
from random import randint
from tqdm import tqdm
class Node:
    """
    Node class, defining the strucutre of a Node for 2D as well as 3D

    Attributes
    -----------
    nDim: int 
        -> Dimensions
    
    x: float
    y: float
    (z: float)
    """
    def __init__(self,scale = 1,*args):
        if int(args[0]) < 0: raise ValueError("Negative Node ID")
        else: self.id = int(args[0])
        if len(args) == 3: # id, x, y
            self.nDim = 2
            self.x = float(args[1])*scale
            self.y = float(args[2])*scale

        elif len(args) == 4: # id, x, y, z
            self.nDim = 3
            self.x = float(args[1])*scale
            self.y = float(args[2])*scale
            self.z = float(args[3])*scale

        else: raise ValueError("Invalid number of node arguments: " + str(len(args)))
        
        self.matn = 99
    
class Element:
    """
    Element Class, multiple Nodes together define a Element. 
    4 Nodes for 2D, 8 Nodes for 3D

    Attributes
    -----------
    numNodes: int
    id: int 
    nodes: int list 
        -> ids of the contained nodes
    node_Set: int set
        -> set of contained node ids, can be used for fast lookup if node is in element
    matn: int
        -> Material Number of the element, initialized as 99
    """
    def __init__(self, *args):
        if len(args) < 2: raise ValueError("Too few Arguments for element: " + str(len(args)))
            
        self.numNodes = len(args) - 1
        self.id = int(args[0])
        self.nodes = []
        for a in args[1:]:
            if type(a) == int or len(a) > 0: self.nodes.append(int(a))
        self.node_set = set(self.nodes)
        
        self.matn = 99
        
class NodeSet:
    """
    Collection of nodes with a name, used for boundary node collections as example

    Attributes:
    ------------
    nodes: int list
        -> Nodes contained in the Node set
    name: str
        -> Initialized as <Unnamed set of nodes>
    """
    def __init__(self,*args):
        self.nodes  = []
        self.name = "Unnamed set of nodes"
        
class ElSet:
    """
    Set of multiple Elements, used to link material numbers (Grains) to Elements

    Attributes:
    ------------
    elems: list of int
        -> List of element ids contained in the ElSet
    name: str
        -> initialized as <Unnamed set of elements>
    setMat: int
        -> material number linked to the ElSet
    lookup: int set
        -> Initialized as one, later defined as set of Element ids used for a 
        fast lookup if element is in Elset
    """
    def __init__(self,*args):
        self.elems = []
        self.name = "Unnamed set of elements"
        self.setMat = 1
        self.lookup = None
        
    def get_matn(self):
        '''
        Initialize material number to Elset
        '''
        matn = re.findall("[0-9]+",self.name) #Care! Corresponds to the number set in elset=faceNUMBER, if there is no number der will be no matn
        self.setMat = int(matn[0])

class AbaqusMesh:
    '''
    Class containing all parts of the Mesh

    Attributes:
    ------------
    nodes: Node list
    elems: Element list
    nsets: NodeSet list
    elsets: ElSet list

    -> All initialized as empty lists 
    '''
    def __init__(self,*args):
        self.nodes = []
        self.elems = []
        self.nsets = []
        self.elsets = []

    def initialize_matn(self):
        for elset in self.elsets:
            elset.lookup = set(elset.elems)
        
        for elem in self.elems:
            for es in self.elsets:
                if elem.id in es.lookup:
                    elem.matn = es.setMat
                    continue
        print("Initizialised Material Numbers to Nodes")
    
    def get_node_id(self,x,y,z = None):
        if z == None:       #2D
            for node in self.nodes:
                if node.x == x and node.y == y and node.z == z:
                    return node.id
        else:               #3D
            for node in self.nodes:
                if node.x == x and node.y == y:
                    return node.id

class InpFileParser:
    """
    This class is able to read an Abaqus .inp-file as inputfile and extract the relevant information. The inp-file is
    created by neper and just the relvant functions are implemented.
    -> Initialize with a filename
    -> use Parse method to read and interpret the file
    """
    READ_NODES = 1
    READ_ELEMS = 2
    READ_NSET = 3
    READ_ELSET = 4
    UNKNOWN = 0
    def __init__(self, filename, nodesPerElem):
        self.filename = filename
        self.nodesPerElem = nodesPerElem
        
    def parse(self,scale = 1):
        readMode = InpFileParser.UNKNOWN
        nodes = []
        elements = []
        nsets = []
        elsets = []

        
        with open(self.filename, 'r') as f:
            for lineNumber, line in tqdm(enumerate(f.readlines())):
                #Checking for keywords -> choose parsing mode
                if line.strip().startswith("*"):
                    if  (line.strip().split(',')[0]) == "*Node":
                        readMode = InpFileParser.READ_NODES
                        
                        
                    elif line.strip().split(',')[0] == "*Element":
                        readMode  = InpFileParser.READ_ELEMS
                        continue
                        
                    elif line.strip().split(',')[0] == "*Nset":
                        readMode  = InpFileParser.READ_NSET
                        curNSet = NodeSet()     #Initialize new nodeset
                        #Get the name of the node set
                        pairs = line.split(',')
                        for p in pairs:
                            if p.count('=') == 0: continue
                            else:
                                var, val = p.split('=')
                                var, val = var.strip(), val.strip()
                                if var == 'nset': 
                                    curNSet.name = val
                                    continue
                        
                        nsets.append(curNSet)     
                        
                    elif line.strip().split(',')[0] == "*Elset":
                        readMode  = InpFileParser.READ_ELSET
                        curElSet = ElSet()
                        #Get the name of the Element set 
                        pairs = line.split(',')
                        for p in pairs:
                            if p.count('=') == 0: continue
                            else:
                                var, val = p.split('=')
                                var, val = var.strip(), val.strip()
                                if var == 'elset':
                                    curElSet.name = val
                                    continue
                        
                        curElSet.get_matn()
                        elsets.append(curElSet)

                    else:
                        readMode  = InpFileParser.UNKNOWN    #Skips all lines, while parser is in unknown mode
                        continue
                        
                elif line.strip() == "":
                    continue
                else:
                    #Parse Nodes
                    if readMode == InpFileParser.READ_NODES:
                        x = Node(scale,*line.strip().split(','))
                        nodes.append(x)
                       
                    #Parse Elements
                    elif readMode == InpFileParser.READ_ELEMS:
                        ints = []
                        for s in line.strip().split(','):
                            if s!= "": ints.append(int(s))
                        x = Element(*ints)
                        if x.numNodes != self.nodesPerElem: 
                            raise ValueError("Parsed element with wrong number of nodes (" + str(len(ints)) + ") at line " + str(lineNumber))
                        elements.append(x)
                
                          
                    #Parse Node Sets
                    elif readMode == InpFileParser.READ_NSET:
                        for s in line.strip().split(','):
                            if s.strip()!="": curNSet.nodes.append(int(s))
                    
                    #Parse Element Sets
                    elif readMode == InpFileParser.READ_ELSET:
                        for e in line.strip().split(','):
                            if e.strip()!="": curElSet.elems.append(int(e))
                    
                    #Skip anything else
                    elif readMode == InpFileParser.UNKNOWN:
                        print('Line ' + str(lineNumber) + ' ignored')
                    
                
            print('Parsed ' + str(len(nodes)) + ' nodes and ' + str(len(elements)) + ' elements')
                
            mesh = AbaqusMesh()
            mesh.nodes = nodes
            mesh.elems = elements
            mesh.nsets = nsets
            mesh.elsets = elsets
            mesh.initialize_matn()
            
            return mesh
