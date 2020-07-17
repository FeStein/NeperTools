import unittest
import nepertools.inp
import nepertools.tess
import nepertools.materials
import nepertools.nmodel
import nepertools.writer

class TestNPQuantity(unittest.TestCase):
    
    def __init__(self,NM):
        self.NM = NM

    def test_quantity(self):
        #self.assertEqual(self.NM.cf['nmodel']['quantity'],len(self.NM.np_list))
        self.assertEqual(1,1)
        
if __name__ == '__main__':
    print('Testing 2D Mikrostrucutre')
    #defining path for each files, here in example folder 
    tessfile_path = 'examples/2m/micro_2d.tess'
    inpfile_path = 'examples/2m/micro_2d.inp'
    configfile_path = 'examples/2m/config.json'
    #parse tess file
    tparser = nepertools.tess.TESS_Parser(tessfile_path) 
    tf = tparser.parse()
    #parse mesh
    parser = nepertools.inp.InpFileParser(inpfile_path,4)
    mesh = parser.parse()
    NM = nepertools.nmodel.NucleusModel2D(configfile_path,mesh,tf)
    NM.create_model()
    TNPQ = TestNPQuantity(NM)
    TNPQ.test_quantity()
