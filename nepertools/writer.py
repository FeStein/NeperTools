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
        self.user_element_number = cf['general']['user_element_number']

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
                f.write('FEAP * * elmt' + str(self.user_element_number) + ': Embedded Grain\n')
                if self.mat_variants == 12:
                    f.write('  ' + str(len(self.mesh.nodes)) + ' ' + str(len(self.mesh.elems)) + ' ' + str(len(self.mesh.elsets)) + ' 3 15 8 0 0\n')
                if self.mat_variants == 3:
                    f.write('  ' + str(len(self.mesh.nodes)) + ' ' + str(len(self.mesh.elems)) + ' ' + str(len(self.mesh.elsets)) + ' 3 7 8 0 0\n')
                f.write('\n')
                f.write('!-------------------Sturcture Informations--------------------------')
                f.write('!edge length:          ' + str(self.cf['general']['scale']) + '\n')
                f.write('!elements   :          ' + str(len(self.mesh.elems)) + '\n')
                f.write('!martensite variants:  ' + str(self.cf['general']['mat_variants']) + '\n')
                f.write('!number of nuclei:     ' + str(self.cf['nmodel']['quantity']) + '\n')
                f.write('!radius of nuclei:     ' + str(self.cf['general']['scale']*self.cf['nmodel']['radius']) + '\n')
                f.write('\n')
                
                f.write('! --------------------------------------------\n')
                f.write('!                    CONSTANTS                \n')
                f.write('! --------------------------------------------\n')
                f.write('\nCONStants\n')
                f.write('L =  ' + "{:e}".format(L) + '  ! M-Mobility parameter \n')
                f.write('M =  ' + "{:e}".format(M) + '  ! pre-factor: kappa_sep \n')
                f.write('op = ' + "{:e}".format(op) + '  ! order of the nucleation sites  \n')
                f.write('dd = ' + "{:e}".format(dd) + '  ! driving force  \n')
                if type(G) == str:
                    f.write('G =  ' + G + '  ! G-Interface energy density \n')
                else:
                    f.write('G =  ' + "{:e}".format(G) + '  ! G-Interface energy density \n')
                f.write('k = 1.0\n')
                if len(self.cf['materials']['irrevers'].split[' '] > 2):
                    splt = self.cf['materials']['irrevers'].split[' ']
                    f.write('sr = ' + splt[0] + ' !Switch irreversibility\n')
                    f.write('st = ' + splt[1] + ' ! Tolerance\n')
                else:
                    f.write('sr = 1     !Switch irreversibility\n')
                    f.write('st = 1e-8 ! Tolerance')
                f.write('si = ' + self.cf['materials']['interpol'] + ' Switch interpolation function, Currently No. 1 and 5 are implemented, default is 5')
                f.write('a = ' + "{:e}".format(scale) + '\n')

            #2D, 2 martensite variants
            elif self.mat_variants == 2:
                f.write('FEAP * * elmt' + str(self.user_element_number) + ': Embedded Grain\n')
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
        sc = self.cf['general']['scale']
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
                f.write('EBOUndary\n')
                f.write('  1 a   1 1 1 1\n')
                f.write('  1 0   1 1 1 1\n')
                f.write('  2 a   1 1 1 1\n')
                f.write('  2 0   1 1 1 1\n')
                f.write('\n')

            #3D 3 mart-variants:    
            elif self.mat_variants == 3:
                f.write("\n")
                f.write("!-----------------------------------------\n")
                f.write("!        Boundary Conditions              \n")
                f.write("!-----------------------------------------\n")
                f.write("\n") 
                f.write("!BOUNdary\n")
                f.write("!1     1  0  0  0 -1  0  0  0\n")
                f.write('!' + str(len(self.mesh.nodes)) + " 0  0  0  0  1  0  0  0\n")
                f.write('!' + str(self.mesh.get_node_id(0.0,0.0,0.0)) + '   0  1  1  1  1  0  0  0\n')            
                f.write('!' + str(self.mesh.get_node_id(max([node.x for node in self.mesh.nodes]),0.0,0.0)) + '   0  0  1  1  1  0  0  0\n')
                f.write('!' + str(self.mesh.get_node_id(0.0,max([node.y for node in self.mesh.nodes]),0.0)) + '   0  0  0  1  1  0  0  0\n')
                f.write('\n')

                f.write("DISPlacement\n")
                f.write("  " + str(self.mesh.nodes[0].id) + " 1 0 0 0 Ts 0 0 0 \n")
                f.write("  " + str(self.mesh.nodes[-1].id) + " 0 0 0 0 Ts 0 0 0 \n")
                f.write("\n")

                f.write('EBOUndary\n')
                f.write('  1 a   1 1 1 1 1 1 1\n')
                f.write('  1 0   1 1 1 1 1 1 1\n')
                f.write('  2 a   1 1 1 1 1 1 1\n')
                f.write('  2 0   1 1 1 1 1 1 1\n')
                f.write('  3 a   1 1 1 1 1 1 1\n')
                f.write('  3 0   1 1 1 1 1 1 1\n')
                
                f.write("\n")

            #3D 12 mart-variants:
            elif self.mat_variants == 12:
                f.write("\n")
                f.write("!-----------------------------------------\n")
                f.write("!        Boundary Conditions              \n")
                f.write("!-----------------------------------------\n")
                f.write("\n") 

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

                f.write('!BOUNdary\n')
                f.write('!  1 0            1 1 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('!  ' + str(self.mesh.get_node_id(0.0,0.0,0.0)) +' 0      0 1 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('!  ' + str(self.mesh.get_node_id(max([node.x for node in self.mesh.nodes]),0.0,0.0)) + '0  0 0 1   0 0 0 0 0 0 0 0 0\n')
                f.write('!  0 0 0 \n')
                f.write('!  \n')     #Will be continued from Nucleus Writer for optional lock of boundaries

            else:
                raise ValueError('Unkown number of martensite variants')
        print('Printed Mesh')


class NucleusWriter():
    '''
    Appends initial conditions as well as solve script to before generated FEAP
    input script. Note that the prior input skript needs to be created before 
    '''
    def __init__(self,filename,config_filename,nucleus_model):
        with open(config_filename) as config_file:
            cf = json.load(config_file) 
        self.cf = cf
        self.filename = filename
        self.nucleus_model = nucleus_model
        self.mat_variants = self.cf['general']['mat_variants']

    def write_np(self):
        if self.mat_variants == 2: #2D Variants
            with open(self.filename,'a') as f:
                if self.cf['nmodel']['lock_bound']:
                    f.write("BOUNdary\n")
                    for node in self.nucleus_model.removed_nodes:
                        f.write('  ' + str(node.id) + ' 0.0 0 0 1 1\n')
                    f.write('\n')
                #Initial Conditions
                f.write('end\n')
                f.write('\n')
                f.write("! -------------------------------------------- \n")
                f.write("!              INITIAL CONDITIONS              \n")
                f.write("! -------------------------------------------- \n")
                f.write(" \n")
                f.write("batch \n")
                f.write("  OPTI \n")
                f.write("  INITial,disp \n")
                f.write("end \n")
                f.write("  " + str(self.nucleus_model.mesh.nodes[0].id) + " 0.0 0.0 0 0 \n")
                f.write("  " + str(self.nucleus_model.mesh.nodes[-1].id) + " 0 0.0 0.0 0 0 \n")
                
                written_node_id_set = set()
                for NP in self.nucleus_model.np_list:
                    for node in NP.nodes:
                        if NP.mvariant == 1:
                            if node.id not in written_node_id_set:
                                written_node_id_set.add(node.id)
                                f.write("  " + str(node.id) + " 0 0.0 0.0 op 0 \n")
                        if NP.mvariant == 2:
                            if node.id not in written_node_id_set:
                                written_node_id_set.add(node.id)
                                f.write("  " + str(node.id) + " 0 0.0 0.0 0 op \n")
                
                #Solve Skript 
                f.write('\n')
                f.write('Batch\n')
                f.write('  ENERgy\n')
                f.write('  TPLOT\n')
                f.write('end\n')
                f.write('energy\n')
                f.write('\n')
                f.write('BATCh\n')
                f.write('    TRANs,BACK\n')
                f.write('    DT,,2e-12 \n')
                f.write('    LOOP,INIT,10\n')
                f.write('        UTANG,,1\n')
                f.write('    NEXT,INIT\n')
                f.write('    !EPRINT\n')
                f.write('    STRE,NODE\n')
                f.write('    PVIEw,TIME\n')
                f.write('    AUTO, DT, 1e-12,1e-3 \n')
                f.write('    AUTO, TIME, 6, 10, 40\n')
                f.write('    LOOP,print,30\n')
                f.write('        LOOP,TIME,10\n')
                f.write('            TIME\n')
                f.write('            LOOP,SOLV,40\n')
                f.write('            UTANG,,1\n')
                f.write('            !EPRINT\n')
                f.write('            NEXT,SOLV\n')
                f.write('            STRE,NODE\n')
                f.write('            PLOT,WIPE\n')
                f.write('            PLOT,CONT,3\n')
                f.write('            NEXT,TIME\n')
                f.write('        PVIEw,TIME\n')
                f.write('    NEXT,print\n')
                f.write('END batch\n')
    
        elif self.mat_variants == 3:
            with open(self.filename,'a') as f:
                if self.cf['nmodel']['lock_bound']:
                    for node in self.nucleus_model.dup_node_list:
                        f.write('  ' + str(node.id) + ' 0.0 0 0 1 1 1\n')
                    f.write('\n')
                f.write('end\n')
                f.write('\n')
                f.write("!-----------------------------------------\n")
                f.write("!        Initial Conditions               \n")
                f.write("!-----------------------------------------\n")
                f.write("\n")
                f.write("batch\n")
                f.write("  OPTI\n")
                f.write("  INITial,disp\n")
                f.write("end\n")
                f.write('1 1 0 0 Ts 0 0 \n')
                f.write(str(self.nucleus_model.mesh.nodes[-1].id) + ' 0 0 0 Ts 0 0\n')
                written_node_set = set()
                for np in self.nucleus_model.np_list:
                    for node in np.nodes:
                        if node not in written_node_set:
                            suffix = "0 "*(np.mvariant-1) + "op " + "0 "*(self.nucleus_model.mat_variants - np.mvariant)
                            f.write("  " + str(node.id) + " 0 0.0 0.0 0.0 Ts " + suffix + "\n")
                            written_node_set.add(node)
                f.write('\n\n\n')
                f.write('interactive\n')
                f.write('\n')
                f.write('batch\n')
                f.write('    GRAPh,,96\n')
                f.write('    OUTDomains\n')
                f.write('end\n')
                f.write('\n')
                f.write('stop\n')
            #12 martensite variants
        elif self.mat_variants == 12:
            with open(self.filename,'a') as f:
                if self.cf['nmodel']['lock_bound']:
                    f.write("!BOUNdary\n")
                    for node in self.nucleus_model.dup_node_list:
                        f.write('!  ' + str(node.id) + ' 0            0 0 0   1 1 1 1 1 1 1 1 1\n')
                        f.write('!  1 1 1 \n')
                    f.write('\n')
                f.write('end\n')
                f.write('\n')
                f.write("!-----------------------------------------\n")
                f.write("!        Initial Conditions               \n")
                f.write("!-----------------------------------------\n")
                f.write("\n")
                f.write("batch\n")
                f.write("  OPTI\n")
                f.write("  INITial,disp\n")
                f.write("end\n")
                f.write('  ' + str(self.nucleus_model.mesh.nodes[0].id) + '     1  1e-20 0.0 0.0   0 0 0 0 0 0 0 0 0 0 0\n')
                f.write('     0\n')
                f.write('  ' + str(self.nucleus_model.mesh.nodes[-1].id) + '     0  1e-20 0.0 0.0   0 0 0 0 0 0 0 0 0 0 0\n')
                f.write('     0\n')
                written_node_set = set()
                for np in self.nucleus_model.np_list:
                    for node in np.nodes:
                        if node not in written_node_set:
                            if np.mvariant == 12:
                                f.write("  " + str(node.id) + " 0 0.0 0.0 0.0 0 0 0 0 0 0 0 0 0 0 0 \n")
                                f.write("    op\n")
                            else:
                                suffix = "0 "*(np.mvariant-1) + "op " + "0 "*(self.nucleus_model.mat_variants - np.mvariant - 1)
                                f.write("  " + str(node.id) + " 0 0.0 0.0 0.0 " + suffix + "\n")
                                f.write("    0\n")
                            written_node_set.add(node)
                f.write('\n\n\n')
                f.write('interactive\n')
                f.write('\n')
                f.write('batch\n')
                f.write('    GRAPh,,108\n')
                f.write('    OUTDomains\n')
                f.write('end\n')
                f.write('\n')
                f.write('stop\n')
        else:
            raise ValueError("Unknown number of martensite variants")

        print('Printed initial conditions')