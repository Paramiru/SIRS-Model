from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
from utils import infectednn

class SIRSModel():
    def __init__(self, nstep=1000, l=0, seed=14122000, p1=0, p2=0, p3=0):
        self.nstep = nstep
        self.l = l if l else int(input("length of lattice: "))
        self.rng = np.random.default_rng(seed)
        self.state = self.rng.choice(3, size=(self.l, self.l))
        self.values = np.unique(self.state.ravel())
        self.p1 = p1 if p1 else float(input("p1, probability of becoming infected: "))
        self.p2 = p2 if p2 else float(input("p2, probability of getting recovered: "))
        self.p3 = p3 if p3 else float(input("p3, probability of becoming susceptible: "))

    def updateCells(self):
        temporaryArray = np.copy(self.state)
        for row in range(self.l):
            for col in range(self.l):
                site = temporaryArray[row,col]
                if site == 0:
                    if infectednn(self.state, row, col):
                        if self.rng.random() < self.p1:
                            self.state[row,col] = 1
                elif site == 1:
                    if self.rng.random() < self.p2:
                        self.state[row,col] = 2
                elif site == 2:
                    if self.rng.random() < self.p3:
                        self.state[row,col] = 0

    def animate(self):
        fig = plt.figure(figsize=(8,4))
        plt.suptitle('SIRS Model', fontsize=16)
        cmap = ListedColormap(["black", "red", "blue"])
        for epoch in range(1, self.nstep+1):
            print(f"Epoch number {epoch}")
            print(f"Infected frac: {np.sum(self.state[self.state==1])/self.l**2}")
            self.updateCells()
            plt.cla()
            im = plt.imshow(self.state, animated=True, vmin=0, vmax=2, interpolation=None, cmap=cmap)
            plt.draw()
            plt.pause(0.0001)

    def getPhaseDiagram(self):
        self.p1, self.p2, self.p3 = 0.0, 0.5, 0.0
        ps = np.arange(0.0, 1+0.05, step=0.05)
        meas = []
        p1s = []
        p3s = []
        for p1 in ps:
            self.p1 = p1
            for p3 in ps:
                self.p3 = p3
                self.state = self.rng.choice(3, size=(self.l, self.l))
                infected = []
                print(f"p1: {self.p1:1f}, p3: {self.p3:1f}")
                print(f"State starts with {np.sum(self.state[self.state == 1])} infected\n")
                for epoch in range(1, 1000+1):
                    self.updateCells()
                    # print(np.sum(self.state[self.state == 1]))
                    if epoch > 100:
                        infected.append(np.sum(self.state[self.state == 1]))
                infected_mean = np.mean(infected)
                print(f"infected mean {infected_mean}\n")
                meas.append(infected_mean)
                p1s.append(self.p1)
                p3s.append(self.p3)
        meas = np.array(meas) / self.l**2

        data = {'avg_inf_frac': meas, 'p1': p1s, 'p3':p3s }
        pd.DataFrame.from_dict(data).to_csv('avg-inf-frac.csv', index=False)




