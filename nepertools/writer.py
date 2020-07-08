#-------------------------------------------------------------------
#Creation of FEAP Inputskript wihtout the intial conditions
#-------------------------------------------------------------------
import json

class FEAPWriter:
    """
    Writes the given structures into a readable file for FEAP
    """
    
    def __init__(self,output_filename,config_filename,mesh,mat_list):
        with open(config_filename) as config_file:
            cf = json.load(config_file) 
        self.cf = cf
        self.filename = output_filename
        self.mesh = mesh
        self.mat_list = mat_list
        self.mat_variants = cf['general']['mat_variants']

    def write_materials(self):
        L = self.cf['constants']['L']
        M = self.cf['constants']['M']
        ks = self.cf['constants']['ks']
        kg = self.cf['constants']['kg']
        al = self.cf['constants']['al']
        Ti = self.cf['constants']['Ti']
        la = self.cf['constants']['la']
        c = self.cf['constants']['c']
        ro = self.cf['constants']['ro']
        ga = self.cf['constants']['ga']
        th = self.cf['constants']['th']
        T0 = self.cf['constants']['T0']
        Ts = self.cf['constants']['Ts']
        op = self.cf['constants']['op']
        dd = self.cf['constants']['dd']
        aa = self.cf['constants']['aa']
        G = self.cf['constants']['G']
        scale = self.cf['general']['scale']
        with open(self.filename,"w+") as f:
            if self.mat_variants == 3 or self.mat_variants == 12:
                f.write('FEAP * * elmt24: Embedded Grain\n')
                if self.mat_variants == 12:
                    f.write('  ' + str(len(self.mesh.nodes)) + ' ' + str(len(self.mesh.elems)) + ' ' + str(len(self.mesh.elsets)) + ' 3 15 8 0 0\n')
                if self.mat_variants == 3:
                    f.write('  ' + str(len(self.mesh.nodes)) + ' ' + str(len(self.mesh.elems)) + ' ' + str(len(self.mesh.elsets)) + ' 3 7 8 0 0\n')
                f.write('! --------------------------------------------\n')
                f.write('!                    CONSTANTS                \n')
                f.write('! --------------------------------------------\n')
                f.write('\nCONStants\n')
                f.write('L =  ' + "{:e}".format(L) + '  ! M-Mobility parameter \n')
                f.write('M =  ' + "{:e}".format(M) + '  ! pre-factor: kappa_sep \n')
                f.write('ks = ' + "{:e}".format(ks) + '  ! pre-factor: kappa_sep \n')
                f.write('kg = ' + "{:e}".format(kg) + '  ! pre-factor: kappa_grad \n')
                f.write('al = ' + "{:e}".format(al) + '  ! alpha-Constant thermal expansion coefficient \n')
                f.write('Ti = ' + "{:e}".format(Ti) + '  ! initial Temperature \n')
                f.write('la = ' + "{:e}".format(la) + '  ! heat conductivity \n')
                f.write('c =  ' + "{:e}".format(c) + '  ! heat capacity \n')
                f.write('ro = ' + "{:e}".format(ro) + '  ! density \n')
                f.write('ga = ' + "{:e}".format(ga) + '  ! parameter for temperature dependend landau polynom: gamma \n')
                f.write('th = ' + "{:e}".format(th) + '  ! parameter for temperature dependend landau polynom: theta^thilde \n')
                f.write('T0 = ' + "{:e}".format(T0) + '  ! parameter for temperature dependend landau polynom: equlibirium temperature \n')
                f.write('Ts = ' + "{:e}".format(Ts) + '  ! temperature of the microstructure \n')
                f.write('op = ' + "{:e}".format(op) + '  ! order of the nucleation sites  \n')
                f.write('dd = ' + "{:e}".format(dd) + '  ! driving force  \n')
                f.write('aa = ' + "{:e}".format(aa) + '  ! energy barrier  \n')
                if type(G) == str:
                    f.write('G =  ' + G + '  ! G-Interface energy density \n')
                else:
                    f.write('G =  ' + "{:e}".format(G) + '  ! G-Interface energy density \n')
                f.write('k = 1.0\n')
                f.write('a = ' + "{:e}".format(scale) + '\n')
            #2D, 2 martensite variants
            elif self.mat_variants == 2:
                f.write('FEAP * * elmt25: Embedded Grain\n')
                f.write('  ' + str(len(self.mesh.nodes)) + ' ' + str(len(self.mesh.elems)) + ' ' + str(len(self.mesh.elsets)) + ' 2 4 4 0 0\n\n')
                f.write('! --------------------------------------------\n')
                f.write('!                    CONSTANTS                \n')
                f.write('! --------------------------------------------\n')
                f.write('\nCONStants\n')
                f.write('L =  ' + "{:e}".format(L) + '  ! M-Mobility parameter \n')
                f.write('M =  ' + "{:e}".format(M) + '  ! pre-factor: kappa_sep \n')
                #f.write('ks = ' + "{:e}".format(ks) + '  ! pre-factor: kappa_sep \n')
                #f.write('kg = ' + "{:e}".format(kg) + '  ! pre-factor: kappa_grad \n')
                #f.write('al = ' + "{:e}".format(al) + '  ! alpha-Constant thermal expansion coefficient \n')
                #f.write('Ti = ' + "{:e}".format(Ti) + '  ! initial Temperature \n')
                #f.write('la = ' + "{:e}".format(la) + '  ! heat conductivity \n')
                #f.write('c =  ' + "{:e}".format(c) + '  ! heat capacity \n')
                #f.write('ro = ' + "{:e}".format(ro) + '  ! density \n')
                #f.write('ga = ' + "{:e}".format(ga) + '  ! parameter for temperature dependend landau polynom: gamma \n')
                #f.write('th = ' + "{:e}".format(th) + '  ! parameter for temperature dependend landau polynom: theta^thilde \n')
                #f.write('T0 = ' + "{:e}".format(T0) + '  ! parameter for temperature dependend landau polynom: equlibirium temperature \n')
                #f.write('Ts = ' + "{:e}".format(Ts) + '  ! temperature of the microstructure \n')
                f.write('op = ' + "{:e}".format(op) + '  ! order of the nucleation sites  \n')
                f.write('dd = ' + "{:e}".format(dd) + '  ! driving force  \n')
                f.write('aa = ' + "{:e}".format(aa) + '  ! energy barrier  \n')
                if type(G) == str:
                    f.write('G =  ' + G + '  ! G-Interface energy density \n')
                else:
                    f.write('G =  ' + "{:e}".format(G) + '  ! G-Interface energy density \n')
                f.write('k = 1.0\n')
                f.write('a = ' + "{:e}".format(scale) + '\n')
            f.write('\n! --------------------------------------------\n')
            f.write('!                    Materials                \n')
            f.write('! --------------------------------------------\n\n')
            
            for mat in self.mat_list:
                for line in mat.content:
                    f.write(line)
                    
        print("Printed Materials")

    def write_mesh(self,sc = 1):
        dim = self.cf['general']['dimensions']
        with open(self.filename, 'a') as f:
            #insert header here
            #Print Coordinates to file
            f.write("!-----------------------------------------\n")
            f.write("!                 Mesh                    \n")
            f.write("!-----------------------------------------\n")
            f.write("\n")
            f.write("COORdinates\n")
            for n in self.mesh.nodes:
                if dim ==2:
                    f.write("  " + str(n.id) + " 0 " + "{:e}".format(n.x*sc) + " " + "{:e}".format(n.y*sc) + "\n")
                elif dim == 3:
                    f.write("  " + str(n.id) + " 0 " + "{:e}".format(n.x*sc) + " " + "{:e}".format(n.y*sc) + " " + "{:e}".format(n.z*sc) + "\n")
  
            #Print Elements to File
            f.write("\n")
            f.write("ELEMents\n")
            for e in self.mesh.elems:
                s = "  " + str(e.id) + " 1 " + str(e.matn)
                for n in e.nodes:
                    s += " " + str(n)
                s += "\n"
                
                f.write(s)
            #2D 2 mart-variants:
            if self.mat_variants == 2:
                f.write("\n")
                f.write("!-----------------------------------------\n")
                f.write("!        Boundary Conditions              \n")
                f.write("!-----------------------------------------\n")
                f.write("\n") 
                f.write('cboun\n')
                f.write('node 0.0,0.0 1 1\n')
                f.write('\n')
                f.write('cboun\n')
                f.write(' node a 0.0 0 1\n')
                f.write('\n')
                f.write('end\n')
                f.write('\n')

            #3D 3 mart-variants:    
            elif self.mat_variants == 3:
                f.write("\n")
                f.write("!-----------------------------------------\n")
                f.write("!        Boundary Conditions              \n")
                f.write("!-----------------------------------------\n")
                f.write("\n") 
                f.write("BOUNdary\n")
                f.write("1     1  0  0  0 -1  0  0  0\n")
                f.write(str(len(self.mesh.nodes)) + " 0  0  0  0  1  0  0  0\n")
                f.write(str(self.mesh.get_node_id(0.0,0.0,0.0)) + '   0  1  1  1  1  0  0  0\n')            
                f.write(str(self.mesh.get_node_id(max([node.x for node in self.mesh.nodes]),0.0,0.0)) + '   0  0  1  1  1  0  0  0\n')
                f.write(str(self.mesh.get_node_id(0.0,max([node.y for node in self.mesh.nodes]),0.0)) + '   0  0  0  1  1  0  0  0\n')
                f.write('\n')

                f.write("DISPlacement\n")
                f.write("  " + str(self.mesh.nodes[0].id) + " 1 0 0 0 Ts 0 0 0 \n")
                f.write("  " + str(self.mesh.nodes[-1].id) + " 0 0 0 0 Ts 0 0 0 \n")
                f.write("\n")

                f.write('!EBOUndary\n')
                f.write('!  1 a   1 1 1 1 1 1 1\n')
                f.write('!  1 0   1 1 1 1 1 1 1\n')
                f.write('!  2 a   1 1 1 1 1 1 1\n')
                f.write('!  2 0   1 1 1 1 1 1 1\n')
                f.write('!  3 a   1 1 1 1 1 1 1\n')
                f.write('!  3 0   1 1 1 1 1 1 1\n')
                
                f.write("\n")
                f.write("end\n")
                f.write("\n")

            #3D 12 mart-variants:
            elif self.mat_variants == 12:
                f.write("\n")
                f.write("!-----------------------------------------\n")
                f.write("!        Boundary Conditions              \n")
                f.write("!-----------------------------------------\n")
                f.write("\n") 

                f.write('!BOUNdary\n')
                f.write('!  1 0            1 1 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('!  ' + str(self.mesh.get_node_id(0.0,0.0,0.0)) +' 0      0 1 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('!  ' + str(self.mesh.get_node_id(max([node.x for node in self.mesh.nodes]),0.0,0.0)) + '0  0 0 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('  \n')

                f.write('EBOUndary     \n')
                f.write('  1 a   1 1 1  1 1 1 1 1 1 1 1 1 1 1\n')
                f.write('        1 \n')
                f.write('  1 0   1 1 1  1 1 1 1 1 1 1 1 1 1 1\n')
                f.write('        1 \n')
                f.write('  2 a   1 1 1  1 1 1 1 1 1 1 1 1 1 1\n')
                f.write('        1 \n')
                f.write('  2 0   1 1 1  1 1 1 1 1 1 1 1 1 1 1 \n')
                f.write('        1 \n')
                f.write('  3 a   1 1 1  1 1 1 1 1 1 1 1 1 1 1\n')
                f.write('        1 \n')
                f.write('  3 0   1 1 1  1 1 1 1 1 1 1 1 1 1 1\n')
                f.write('        1 \n')

                f.write('\n')
                f.write("end\n")
                f.write("\n")

            else:
                raise ValueError('Unkown number of martensite variants')
        print('Printed Mesh')