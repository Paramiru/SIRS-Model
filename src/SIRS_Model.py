from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
from utils import infectednn
from numpy.random import SeedSequence
from resampling import get_scaled_var_error

class SIRS_Model():
    def __init__(self, nstep=1000, l=0, seed=None, p1=0, p2=0, p3=0):
        self.nstep = nstep
        self.l = l if l else int(input("length of lattice: "))
        self.rng = np.random.default_rng(SeedSequence(seed))
        self.state = self.rng.choice(3, size=(self.l, self.l))
        self.p1 = p1 if p1 else float(input("p1, probability of becoming infected: "))
        self.p2 = p2 if p2 else float(input("p2, probability of getting recovered: "))
        self.p3 = p3 if p3 else float(input("p3, probability of becoming susceptible: "))

    def update_cell(self, row, col):
        site = self.state[row,col]
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

    def update_cells(self):
        for _ in range(self.l**2):
            pos = self.rng.integers(self.l, size=2)
            self.update_cell(pos[0], pos[1])

    def animate(self):
        plt.figure(figsize=(8,4))
        plt.suptitle('SIRS Model', fontsize=16)
        cmap = ListedColormap(["black", "red", "blue"])
        for epoch in range(1, self.nstep+1):
            print(f"Epoch number {epoch}")
            print(f"Infected frac: {np.sum(self.state[self.state==1])/self.l**2}")
            self.update_cells()
            plt.cla()
            plt.imshow(self.state, animated=True, vmin=0, vmax=2, interpolation=None, cmap=cmap)
            plt.draw()
            plt.pause(0.001)

    def get_infected_cells(self):
        return np.sum(self.state[self.state==1])

    def get_phase_diags(self):
        self.p1, self.p2, self.p3 = 0.0, 0.5, 0.0
        ps = np.arange(0.0, 1+0.05, step=0.05)
        means, vars, p1s, p3s = [], [], [], []
        mean_contour_plot = np.zeros((len(ps), len(ps)))
        var_contour_plot = np.zeros((len(ps), len(ps)))
        for i in range(len(ps)):
            self.p1 = ps[i]
            for j in range(len(ps)):
                self.p3 = ps[j]
                # reset array
                self.state = self.rng.choice(3, size=(self.l, self.l))
                infected_cells_meas = []
                print(f"\np1: {self.p1:1f}, p3: {self.p3:1f}")
                print(f"State starts with {np.sum(self.state[self.state == 1])} infected\n")
                for epoch in range(1000):
                    self.update_cells()
                    # wait for 100 epoch for equilibration time
                    infected_cells = self.get_infected_cells()
                    if infected_cells == 0:
                        if epoch < 100:
                            infected_cells_meas.append(0)
                        break
                    if epoch >= 100: 
                        # take measurement of infected cells in every epoch
                        infected_cells_meas.append(infected_cells)
                mean = np.mean(infected_cells_meas)
                means.append(mean / self.l**2)
                print(f"Mean of infected sites: {means[-1]}")
                var = np.var(infected_cells_meas)
                vars.append(var / self.l**2)
                print(f"Variance of infected siteds: {vars[-1]}")
                p1s.append(self.p1)
                p3s.append(self.p3)
                mean_contour_plot[len(ps)-1-i, j] = mean / self.l**2
                var_contour_plot[len(ps)-1-i, j] = var / self.l**2

        plt.imshow(mean_contour_plot, extent=[0,1,0,1])
        plt.colorbar()
        plt.savefig('mean_contour_plot10.png')
        plt.show()
        plt.clf()
        plt.imshow(var_contour_plot, extent=[0,1,0,1])
        plt.colorbar()
        plt.savefig('var_contour_plot10.png')
        plt.show()

        data = {'scaled_mean': means, 'p1': p1s, 'p3':p3s }
        pd.DataFrame.from_dict(data).to_csv('scaled_mean' + '.csv', index=False)

        data = {'scaled_var': vars, 'p1': p1s, 'p3':p3s }
        pd.DataFrame.from_dict(data).to_csv('scaled_var' + '.csv', index=False)

    def get_scaled_var(self):
        self.p2, self.p3 = 0.5, 0.5
        p1s = np.arange(0.25, 0.4, step=0.01)
        scaled_vars, error_bars = [], []
        for self.p1 in p1s:
            print(f"\nUsing probability p1: {self.p1:.2f}")
            self.state = self.rng.choice(3, size=(self.l, self.l))
            infected_cells = []
            for epoch in range(int(1e4)):
                self.update_cells()
                if epoch >= 100:
                    infected_cells.append(self.get_infected_cells())
            scaled_vars.append(np.var(infected_cells) / self.l**2)
            print(f"Scaled variance: {scaled_vars[-1]:.2f}")
            error_bars.append(get_scaled_var_error(infected_cells, self.l**2))
            print(f"Error bar: {error_bars[-1]:.2f}")

        data = {'p1': p1s, 'scaled_var': scaled_vars, 'error_bars': error_bars}
        pd.DataFrame.from_dict(data).to_csv('scaled_variance.csv', index=False)

        plt.errorbar(p1s, scaled_vars, error_bars, fmt='o', capsize=3)
        plt.show()
        
        



