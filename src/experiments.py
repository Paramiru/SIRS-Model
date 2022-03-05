from SIRSModel import SIRSModel


def exp1():
    model = SIRSModel(l=50,p1=0.8, p2=0.5, p3=0.8)
    model.animate()
    
def exp2():
    model = SIRSModel(l=50,p1=0.8, p2=0.5, p3=0.8)
    model.getPhaseDiagram()

if __name__ == "__main__":
    # exp1()
    exp2()
