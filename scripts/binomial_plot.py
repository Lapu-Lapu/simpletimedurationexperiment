import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.ticker import MaxNLocator

N = 30
p = 0.8
theta = stats.binom(N, p)
r = np.arange(10, N, dtype=int)
fig = plt.figure()
ax = fig.gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_title(f'Binomial Distribution (N={N}; $\Theta$={p})')
ax.set_xlabel('$r_{ij}$')
ax.set_ylabel('$p(r_{ij})$')
ax.bar(r, theta.pmf(r))
plt.savefig('figures/Binomial_Example.png')
plt.close()
