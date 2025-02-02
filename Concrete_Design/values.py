
from FE_code.model import Model



class Values:
    
    def __init__(self):
        self._dsl = 20
        self._dbu = 10
        self.c_nom_l = 0
        self.c_nom_b = 0
        self.mue_eds = []
        self.omega_1 = []
        self.sigma_sd = []

    @property
    def dsl(self):
        return self._dsl
    @dsl.setter
    def dsl(self, value):
        self._dsl = value

    @property
    def dbu(self):
        return self._dbu
    @dbu.setter
    def dbu(self, value):
        self._dbu = value

    def concrete(self, concrete_type):

        if concrete_type == 'c1215':
            c = {'fck': 12, 'fcd': 0.85*12/1.5, 'fctm': 1.6, 'fctk,0.05': 1.1, 'Ecm': 27000}
        elif concrete_type == 'c1620':
            c = {'fck': 16, 'fcd': 0.85*16/1.5, 'fctm': 1.9, 'fctk,0.05': 1.3, 'Ecm': 29000}
        elif concrete_type == 'c2025':
            c = {'fck': 20, 'fcd': 0.85*20/1.5, 'fctm': 2.2, 'fctk,0.05': 1.5, 'Ecm': 30000}
        elif concrete_type == 'c2530':
            c = {'fck': 25, 'fcd': 0.85*25/1.5, 'fctm': 2.6, 'fctk,0.05': 1.8, 'Ecm': 31000}
        elif concrete_type == 'c3037':
            c = {'fck': 30, 'fcd': 0.85*30/1.5, 'fctm': 2.9, 'fctk,0.05': 2.0, 'Ecm': 33000}
        elif concrete_type == 'c3545':
            c = {'fck': 35, 'fcd': 0.85*35/1.5, 'fctm': 3.2, 'fctk,0.05': 2.2, 'Ecm': 34000}
        elif concrete_type == 'c4050':
            c = {'fck': 40, 'fcd': 0.85*40/1.5, 'fctm': 3.5, 'fctk,0.05': 2.5, 'Ecm': 35000}
        elif concrete_type == 'c4555':
            c = {'fck': 45, 'fcd': 0.85*45/1.5, 'fctm': 3.8, 'fctk,0.05': 2.7, 'Ecm': 36000}
        elif concrete_type == 'c5060':
            c = {'fck': 50, 'fcd': 0.85*50/1.5, 'fctm': 4.1, 'fctk,0.05': 2.9, 'Ecm': 37000}
        else:
            raise ValueError(f'concrete_type: {concrete_type} is undefined')

        return c

    def steel(self):
        fyk = 500

        return fyk

    def check_exposition_class(self, exp):
        exposition_class = ('XC1', 'XC2', 'XC3', 'XC4', 
                     'XD1', 'XD2', 'XD3',
                     'XS1', 'XS2', 'XS3'
        )
        if exp not in exposition_class:
            raise ValueError(f'exposition class {exp} is not definded')
        
        return exp


    def concrete_cover(self, exp):

        #dictionary for c_min_dur
        c_min_dur = {'XC1': 10, 'XC2': 20, 'XC3': 20, 'XC4': 25, 
                     'XD1': 30, 'XD2': 35, 'XD3': 40,
                     'XS1': 30, 'XS2': 35, 'XS3': 40
        }
        
                    

        #dictionary for d_c_dur,y
        d_c_dury = {'XC1': 0, 'XC2': 0, 'XC3': 0, 'XC4': 0, 
                    'XD1': 10, 'XD2': 5, 'XD3': 0,
                    'XS1': 10, 'XS2': 5, 'XS3': 0
        }
                    

        c_min_l = self._dsl
        c_min_b = self._dbu
        c_min_dur = c_min_dur[exp]
        d_c_dury = d_c_dury[exp]

        #definition of d_c_dev
        if exp == 'XC1':
            d_c_dev = 10
        elif c_min_dur > c_min_b:
            d_c_dev = 15
        else:
            d_c_dev = 10 

        c_min_l = max(c_min_l, c_min_dur+d_c_dury, 10)
        c_min_b = max(c_min_b, c_min_dur+d_c_dury, 10)

        self.c_nom_l = c_min_l + d_c_dev
        self.c_nom_b = c_min_b + d_c_dev

        return (self.c_nom_b, self.c_nom_l)

    def static_usable_height(self, h, exp):

        self.c_nom_b=self.concrete_cover(exp)[0]
        self.c_nom_l=self.concrete_cover(exp)[1]

        d1 = max(self._dsl/2 + self.c_nom_l, 
                 self._dsl/2 + self._dbu + self.c_nom_b
                )

        d = h - d1*0.001
        
        return d

    def design_table_values(self):
        
        for i in range(41):
            self.mue_eds.append(0.01*i)
        
        self.omega_1 = [0.0000, 0.0101, 0.0203, 0.0306, 0.0410, 0.0515,
                        0.0621, 0.0728, 0.0836, 0.0946, 0.1058, 0.1170,
                        0.1285, 0.1401, 0.1519, 0.1638, 0.1759, 0.1882,
                        0.2007, 0.2134, 0.2263, 0.2395, 0.2529, 0.2665, 
                        0.2804, 0.2946, 0.3091, 0.3239, 0.3391, 0.3546, 
                        0.3706, 0.3869, 0.4038, 0.4211, 0.4391, 0.4576, 
                        0.4768, 0.4968, 0.5177, 0.5396, 0.5627 
                        ]

        self.sigma_sd = [456.5, 456.5, 456.5, 456.5, 456.5, 456.5, 
                         456.5, 456.5, 456.5, 456.5, 454.9, 452.4, 
                         450.4, 448.6, 447.1, 445.9, 444.7, 443.7, 
                         442.8, 442.0, 441.3, 440.6, 440.1, 439.5, 
                         439.0, 438.4, 438.1, 437.7, 437.3, 437.0, 
                         436.7, 436.4, 436.1, 435.8, 435.5, 435.3, 
                         435.0, 434.8, 394.5, 350.1, 307.1  
                        ]
        return (self.mue_eds, self.omega_1, self.sigma_sd)


    def _interpolate(self, value, column):
        # interpolation of mue_eds
       
        i_0, i_1 = None, None
        for i, mue in enumerate(self.mue_eds):
            if mue > value:
                i_1 = i
                i_0 = i-1
                break

        # if i_1 or i_0 <=-5:
        #     raise Exception("Value {} not found in array {}".format(value, self.mue_eds))

        interpolated_value = column[i_0] + (column[i_1]-column[i_0])/(self.mue_eds[i_1]-self.mue_eds[i_0]) * (value-self.mue_eds[i_0])

        return interpolated_value

    def interpolate_omega(self, value):
        return self._interpolate(value, self.omega_1)

    def interpolate_sigma(self, value):
        return self._interpolate(value, self.sigma_sd)

    #TODO: table with number of reinforcement bars

    def reset_values(self):
        self._dsl = 20
        self._dbu = 10
        self.c_nom_l = 0
        self.c_nom_b = 0
        self.mue_eds = []
        self.omega_1 = []
        self.sigma_sd = []




