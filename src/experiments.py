from SIRS_Model import SIRS_Model
from SIRS_Model_Immune import SIRS_Model_Immune


def exp1():
    seed = 96
    # p1, p2, p3 = 0.5, 0.6, 0.1 # absorbing state
    p1, p2, p3 = 0.5, 0.5, 0.5 # dynamic equilibrium 
    # p1, p2, p3 = 0.8, 0.1, 0.01, 69 # cyclic waves
    # p1, p2, p3 = 0.31, 0.5, 0.5
    model = SIRS_Model(l=50, seed=seed, p1=p1, p2=p2, p3=p3)
    model.animate()  

def exp2():
    model = SIRS_Model(l=50, p1=0.5, seed=2442, p2=0.5, p3=0.5)
    model.get_scaled_var(step=0.01)

def exp3():
    model = SIRS_Model_Immune(immune_frac=0.0, l=50, seed=4242, p1=0.5, p2=0.5, p3=0.5)
    model.get_immune_frac_data(step=0.01)

def exp3():
    immune_frac, p1, p2, p3 = 0.2, 0.4, 0.6, 0.7
    model = SIRS_Model_Immune(immune_frac=immune_frac, l=50, seed=4242, p1=p1, p2=p2, p3=p3)
    model.animate()

 
if __name__ == "__main__":
    exp1()

