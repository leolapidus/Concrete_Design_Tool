
from FE_code.model import Model


class Values:
    #TODO: Betondeckung in Abhängigkeit von den Expositionsklassen
    #Druck
    # fcd = 0.85*fck/1,5

    def __init__(self):
        self._dsl = 0
        self._dbu = 0
        self.c_nom_l = 0
        self.c_nom_b = 0

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


    def concrete_cover(self, EXP):

        #dictionary for c_min_dur
        c_min_dur = dict(('XC1', 10), ('XC2', 20), ('XC3', 20), ('XC4', 25), 
                        ('XD1', 30), ('XD2', 35), ('XD3', 40),
                        ('XS1', 30), ('XS2', 35), ('XS3', 40)
                    )

        #dictionary for d_c_dur,y
        d_c_dury = dict(('XC1', 0), ('XC2', 0), ('XC3', 0), ('XC4', 0), 
                        ('XD1', 10), ('XD2', 5), ('XD3', 0),
                        ('XS1', 10), ('XS2', 5), ('XS3', 0)
                    )

        c_min_l = self._dsl
        c_min_b = self._dbu
        c_min_dur = c_min_dur[EXP]
        d_c_dury = d_c_dury[EXP]

        #definition of d_c_dev
        if EXP == 'XC1':
            d_c_dev = 10
        elif c_min_dur > c_min_b:
            d_c_dev = 15
        else:
            d_c_dev = 10 

        c_min_l = max(c_min_l, c_min_dur+d_c_dury, 10)
        c_min_b = max(c_min_b, c_min_dur+d_c_dury, 10)

        c_nom_l = c_min_l + d_c_dev
        c_nom_b = c_min_b + d_c_dev

    def static_usable_height(self, model):

        d1 = max(self._dsl/2 + self.c_nom_l, 
                 self._dsl/2 + self._dbu + self.c_nom_b
                )

        d = model.h - d1
