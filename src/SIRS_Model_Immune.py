import json
from collections import defaultdict

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import sem

from SIRS_Model import SIRS_Model


class SIRS_Model_Immune(SIRS_Model):
    def __init__(self, immune_frac, nstep=1000, l=0, seed=14122000, p1=0, p2=0, p3=0):
        super().__init__(nstep, l, seed, p1, p2, p3)
        self.immune_frac = immune_frac
        self.reset_state()
        
    def reset_state(self):
        p = (1 - self.immune_frac)/3
        self.state = self.rng.choice([-1, 0, 1, 2], size=(self.l, self.l), p=[self.immune_frac, p, p, p])

    def animate(self):
        plt.figure(figsize=(8,4))
        plt.suptitle('SIRS Model', fontsize=16)
        cmap = ListedColormap(["white", "black", "red", "blue"])
        for epoch in range(1, self.nstep+1):
            print(f"Epoch number {epoch}")
            print(f"Infected frac: {self.get_infected_cells()/self.l**2}")
            self.update_cells()
            plt.cla()
            plt.imshow(self.state, animated=True, vmin=-1, vmax=2, interpolation=None, cmap=cmap)
            plt.draw()
            plt.pause(0.001)

    def get_immune_frac_data(self):
        self.p1, self.p2, self.p3 = 0.5, 0.5, 0.5
        immune_fracs = np.arange(0, 1.05, step=0.05)
        results = defaultdict(list)
        num_simulations = 5
        for simulation in range(num_simulations):
            print(f"Simulation {simulation}")

            for self.immune_frac in immune_fracs:
                print(f"Immune fraction: {self.immune_frac}")
                infected_cells_arr = []
                self.reset_state()

                for epoch in range(int(1e3)+100):
                    if epoch % 250 == 0:
                        print(f"Epoch {epoch}")
                        print(f"Infected cells {self.get_infected_cells()}\n")
                    self.update_cells()
                    # 100 epochs for equilibration time
                    infected_cells = self.get_infected_cells()
                    if epoch > 100:
                        infected_cells_arr.append(infected_cells)
                    else:
                        if not infected_cells:
                            infected_cells_arr.append(0)
                            break
                # add fraction of infected cells for a given immune_frac
                results[self.immune_frac].append(np.mean(infected_cells_arr) / self.l**2)

        avg_frac = []
        std_error_mean = []

        tf = open("immunity_data.json", "w")
        json.dump(results,tf)
        tf.close()

        for immune_frac in immune_fracs:
            avg_frac.append(np.mean(results[immune_frac]))
            std_error_mean.append(sem(results[immune_frac]))

        data = {'immune_frac': immune_fracs, 'avg_frac_infected': avg_frac, 'std_error_mean': std_error_mean}
        pd.DataFrame.from_dict(data).to_csv('immunity_data.csv', index=False)
