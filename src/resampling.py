import numpy as np

def get_scaled_var_error(meas, N, k=100):
    scaled_var_resampled = []
    n = len(meas)
    for _ in range(k):
        meas_resampled = np.random.choice(meas, size=n)
        scaled_var_resampled.append(np.var(meas_resampled) / N)
    return np.std(np.array(scaled_var_resampled))
