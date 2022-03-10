from SIRS_Model import SIRS_Model
import numpy as np
from SIRS_Model_Immune import SIRS_Model_Immune


def exp1():
    # p1, p2, p3 = 0.5, 0.6, 0.1 # absorbing state
    # p1, p2, p3 = 0.5, 0.5, 0.5 # dynamic equilibrium 
    p1, p2, p3, seed = 0.8, 0.1, 0.01, 69 # cyclic waves
    # p1, p2, p3 = 0.31, 0.5, 0.5
    model = SIRS_Model(l=50, seed=69, p1=p1, p2=p2, p3=p3)
    model.animate()  

def exp3():
    model = SIRS_Model(l=50, p1=0.5, seed=42, p2=0.5, p3=0.5)
    model.get_scaled_var()

def exp5():
    model = SIRS_Model_Immune(immune_frac=0.0, l=50, seed=42, p1=0.5, p2=0.5, p3=0.5)
    model.get_immune_frac_data()
 
if __name__ == "__main__":
    # exp1()
    exp3()
    # exp3()
    # exp5()
