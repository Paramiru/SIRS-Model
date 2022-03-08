from SIRS_Model import SIRS_Model
import numpy as np
from SIRS_Model_Immune import SIRS_Model_Immune


def exp1():
    # p1, p2, p3 = 0.5, 0.6, 0.1 # absorbing state
    # p1, p2, p3 = 0.5, 0.5, 0.5 # dynamic equilibrium 
    # p1, p2, p3 = 0.8, 0.1, 0.01 # cyclic waves
    p1, p2, p3 = 0.31, 0.5, 0.5
    model = SIRS_Model(l=50, p1=p1, p2=p2, p3=p3)
    model.animate()
    
def exp2():
    model = SIRS_Model(l=50,p1=0.8, p2=0.5, p3=0.8)
    model.get_phase_diag(func=np.var)

def exp3():
    model = SIRS_Model(l=10, p1=0.2, seed=69, p2=0.5, p3=0.5)
    model.get_scaled_var()

def exp4():
    model = SIRS_Model_Immune(immune_frac=0, l=50, p1=0.5, p2=0.5, p3=0.5)
    model.get_immune_frac_data()

def exp5():
    model = SIRS_Model(l=10, seed=42000, p1=0.5, p2=0.5, p3=0.5)
    model.get_phase_diags()

def exp6():
    model = SIRS_Model(l=20,p1=0.8, seed=213412, p2=0.5, p3=0.8)
    model.get_scaled_var()
 
if __name__ == "__main__":
    # exp1()
    # exp2()
    # exp3()
    # exp5()
    exp6()
