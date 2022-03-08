from collections import defaultdict
import numpy as np
from SIRS_Model import SIRS_Model
import pandas as pd

class SIRS_Model_Immune(SIRS_Model):
    def __init__(self, immune_frac, nstep=1000, l=0, seed=14122000, p1=0, p2=0, p3=0):
        super().__init__(nstep, l, seed, p1, p2, p3)
        self.immune_frac = immune_frac
        self.add_immune_cells()
        
    def add_immune_cells(self):
        n = int(self.immune_frac * self.l**2)
        idxs = np.random.choice(self.l, size=(n,2))  
        for row, col in idxs:
            self.state[row, col] = -1

    def get_immune_frac_data(self):
        self.p1, self.p2, self.p3 = 0.5, 0.5, 0.5
        immune_fracs = np.arange(0, 1.1, step=0.1)
        results = defaultdict(list)
        num_simulations = 5
        for simulation in range(num_simulations):
            print(f"Simulation {simulation}")
            for self.immune_frac in immune_fracs:
                print(f"Immune fraction: {self.immune_frac}")
                infected_cells = []
                # reset array
                self.state = self.rng.choice(3, size=(self.l, self.l))
                self.add_immune_cells()
                for epoch in range(int(1e3)):
                    self.update_cells()
                    # 100 epochs for equilibration time
                    if epoch > 100:
                        infected_cells.append(self.get_infected_cells())
                results[self.immune_frac].append(np.mean(infected_cells) / self.l**2)
        avg_frac = []
        std_error_mean = []
        for immune_frac in immune_fracs:
            avg_frac.append(np.mean(results[immune_frac]))
            std_error_mean.append(np.std(results[immune_frac])/np.sqrt(len(results[immune_frac])))

        data = {'immune_frac': immune_fracs, 'avg_frac_infected': avg_frac, 'std_error_mean': std_error_mean}
        pd.DataFrame.from_dict(data).to_csv('immunity_data.csv', index=False)