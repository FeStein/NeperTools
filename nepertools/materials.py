#-------------------------------------------------------------------
#Creation of different materials as FEAP Input for each grain
#-------------------------------------------------------------------
import numpy as np 
import json
from decimal import Decimal

class Material_Creator():
    
    def __init__(self,configfile): #,elasticitys,eigenstrains,mat_variants,irrevers,interpol):
        with open(configfile) as config_file:
            cf = json.load(config_file) 
        self.elasticitys = cf['materials']['elasticitys']
        self.eigenstrains = cf['materials']['eigenstrains']
        self.mat_variants = cf['general']['mat_variants']
        self.irrevers = cf['materials']['irrevers']
        self.interpol = cf['materials']['interpol']
        self.user_element_number = cf['general']['user_element_number']
    def create_material_list(self,phi_list):

        material_list = []
        
        for num,(phi1,phi2,phi3) in enumerate(phi_list):
            current_material = Material(num+1,phi1,phi2,phi3,self.elasticitys,self.eigenstrains,self.irrevers,self.interpol)
            current_material.create_content(self.mat_variants,self.user_element_number)
            material_list.append(current_material)

        self.material_list = material_list
        print('Initialized Materials')

class Material:
    
    def __init__(self,id,phi1,phi2,phi3,elasticitys,eigenstrains,irrevers,interpol):
        self.orientations = [phi1,phi2,phi3]
        self.appendix = [ #The Same for every material
            '    G             L           M            ! G-Interface energy density, L-Controls width of transition zone, M-Mobility parameter \n',
            '    ks           kg                        ! Pre-factors: kappa_sep, kappa_grad \n',
            '    al           Ti                        ! alpha-Constant thermal expansion coefficient, Initial Temperature \n',
            '    la            c                        ! heat conductivity, heat capacity \n',
            '    ro                                     ! density \n',
            '    ga           th            T0          ! parameters for temperature dependend landau polynom \n',
            '    dd           aa                        ! Driving Force and energy barrier \n\n'   
        ]
        self.id = id
        self.content = []

        self.elasticitys = elasticitys
        self.eigenstrains = eigenstrains
        self.irrevers = irrevers
        self.interpol = interpol
        
    def create_content(self,mat_var,user_element_number):
        self.content.append('MATErial,' + str(self.id) + "\n")
        #Material cratiom for 2 martensite variants (useful for 2D)
        if mat_var == 2:
            self.content.append('  User,' + str(user_element_number) + '\n')
            self.content.append('    ' + self.irrevers + '                                                    ! Switch irreversibility (1-on,else-off), Tolerance \n')
            self.content.append('    ' + str(self.interpol) + '                                                         ! Switch interpolation function, Currently No. 1 and 5 implemented, default is 5 \n')
            self.content.append('    dd   G     L     M                                        ! Chem. energy diff., G-Interface energy density, L-Controls width of transition zone, M-Mobility parameter\n')
            self.content.append('    ' + ' '.join([str((ori*np.pi)/180) for ori in self.orientations[:1]]) +' ! Rotation of crystal: Bunge-Euler angles in rad\n' )
            #Create elasticity tensor:
            if len(self.elasticitys) < 2:
                raise ValueError('too few elasticity tensors given, 2 needed')
            for num,et in enumerate(self.elasticitys[:2]):
                if num == 0:
                    l = '    ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '                         ! C_11 C_12 C_44 elasticity tensor austenite \n'
                else:
                    l = '    ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '                         ! C_11 C_12 C_44 elasticity tensor martensite' + str(num) + ' \n'
                self.content.append(l)
            #create eigenstrains:
            if len(self.eigenstrains) < 2:
                raise ValueError('too few eigenstrains given, 2 needed')
            for num,es in enumerate(self.eigenstrains[:2]):
                l = '    ' + ' '.join([str(i) for i in es]) + '  ! E_11 E_22 E_12 Eigenstrain tensor martensite' + str(num + 1) +' \n'
                self.content.append(l)
            self.content.append('\n')


        #Material creation for 3 martensite variants 
        elif mat_var == 3:
            self.content.append('  USER,' + str(user_element_number) + '\n')
            self.content.append('  sr st        !switch irreveresibility (1-on,else-off, Tolerance\n')
            self.content.append('  si           !switch interpolation function, Currently No. 1 and 5 implemented, default is 5')
            self.content.append('  dd  G  L  M  ! G-Interface energy density, L-Controls width of transition zone, M-Mobility parameter')
            #append orientations
            self.content.append('  ' + ' '.join([str((ori*np.pi)/180) for ori in self.orientations]) +'\n' )
            #Create elasticity tensor:
            if len(self.elasticitys) < 4:
                raise ValueError('too few elasticity tensors given, 4 needed')
            for num,et in enumerate(self.elasticitys[:4]):
                if num == 0:
                    l = '  ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '  ! C_11 C_12 C_44 elasticity tensor austenite \n'
                else:
                    l = '  ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '  ! C_11 C_12 C_44 elasticity tensor martensite' + str(num) + ' \n'
                self.content.append(l)
            #create eigenstrains:
            if len(self.eigenstrains) < 3:
                raise ValueError('too few eigenstrains given, 3 needed')
            for num,es in enumerate(self.eigenstrains[:3]):
                l = '  ' + ' '.join([str(i) for i in es]) + '  ! E_11 E_22 E_12 Eigenstrain tensor martensite' + str(num + 1) +' \n'
                self.content.append(l)

            self.content.append('\n')
            #self.content.extend(self.appendix)

        #Material creation for 12 martensite variants
        elif mat_var == 12:
            self.content.append('  USER,' + str(user_element_number) + ', ' + str(self.id) + ',1,2,3,4,5,6,7,8,9,10,11,12,13\n')
            self.content.append('  14,15\n')
            self.content.append('  sr st        !switch irreveresibility (1-on,else-off, Tolerance\n')
            self.content.append('  si           !switch interpolation function, Currently No. 1 and 5 implemented, default is 5\n')
            self.content.append('  dd  G  L  M  ! G-Interface energy density, L-Controls width of transition zone, M-Mobility parameter\n')
            #append orientations
            self.content.append('  ' + ' '.join([str((ori*np.pi)/180) for ori in self.orientations]) +'\n' )
            #Create elasticity tensor:
            if len(self.elasticitys) < 2:
                raise ValueError('too few elasticity tensors given, 2 needed')
            for num,et in enumerate(self.elasticitys[:2]):
                if num == 0:
                    l = '  ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '  ! C_11 C_12 C_44 elasticity tensor austenite \n'
                else:
                    l = '  ' + ' '.join(["{:.6E}".format(Decimal(str(i))) for i in et]) + '  ! C_11 C_12 C_44 elasticity tensor martensite' + str(num) + ' \n'
                self.content.append(l)
            #create eigenstrains:
            if len(self.eigenstrains) < 12:
                raise ValueError('too few eigenstrains given, 12 needed')
            for num,es in enumerate(self.eigenstrains[:12]):
                l = '  ' + ' '.join([str(i) for i in es]) + '  ! E_11 E_22 E_12 Eigenstrain tensor martensite' + str(num + 1) +' \n'
                self.content.append(l)
                
            self.content.append('\n')
            #self.content.extend(self.appendix) Changed behaviour
        else:
            raise ValueError('Unknown number of martesnite variants')