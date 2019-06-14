
from FE_code.model import Model


#TODO: Betondeckung in Abhängigkeit von den Expositionsklassen
#Druck
# fcd = 0.85*fck/1,5


def reinforcement(self):

    _dsl = 0 #mm
    _dbu = 0 #mm
    
@property
def dsl(self):
    return reinforcement._dsl
@dsl.setter
def dsl(self, value):
    reinforcement._dsl = value

@property
def dbu(self):
    return reinforcement._dbu
@dbu.setter
def dbu(self, value):
    reinforcement._dbu = value

def concrete(self):
    c1215 = dict(('fck', 12), ('fctm', 1.6), ('fctk,0.05', 1.1), ('Ecm', 27000))
    c1620 = dict(('fck', 16), ('fctm', 1.9), ('fctk,0.05', 1.3), ('Ecm', 29000))
    c2025 = dict(('fck', 20), ('fctm', 2.2), ('fctk,0.05', 1.5), ('Ecm', 30000))
    c2530 = dict(('fck', 25), ('fctm', 2.6), ('fctk,0.05', 1.8), ('Ecm', 31000))
    c3037 = dict(('fck', 30), ('fctm', 2.9), ('fctk,0.05', 2.0), ('Ecm', 33000))
    c3545 = dict(('fck', 35), ('fctm', 3.2), ('fctk,0.05', 2.2), ('Ecm', 34000))
    c4050 = dict(('fck', 40), ('fctm', 3.5), ('fctk,0.05', 2.5), ('Ecm', 35000))
    c4555 = dict(('fck', 45), ('fctm', 3.8), ('fctk,0.05', 2.7), ('Ecm', 36000))
    c5060 = dict(('fck', 50), ('fctm', 4.1), ('fctk,0.05', 2.9), ('Ecm', 37000))
   



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

    

    c_min_l = reinforcement._dsl #mm
    c_min_b = reinforcement._dbu #mm
    c_min_dur = c_min_dur[EXP] #mm
    d_c_dury = d_c_dury[EXP] #mm

    #definition of d_c_dev

    if EXP == 'XC1':
        d_c_dev = 10 #mm
    elif c_min_dur > c_min_b:
        d_c_dev = 15 #mm
    else:
        d_c_dev = 10 #mm

    c_min_l = max(c_min_l, c_min_dur+d_c_dury, 10) #mm
    c_min_b = max(c_min_b, c_min_dur+d_c_dury, 10) #mm

    c_nom_l = c_min_l + d_c_dev #mm
    c_nom_b = c_min_b + d_c_dev #mm

def static_usable_height(self, model, concrete_cover):

    d1 = max(reinforcement._dsl/2 + concrete_cover.c_nom_l, 
             reinforcement._dsl/2 + reinforcement._dbu + concrete_cover.c_nom_b
            ) #mm

    d = model.h - d1*0.01 #m

#TODO: table with number of reinforcement bars
