import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np


data1 = np.random.normal(10, 2, 1000)
data2 = np.random.normal(20, 2, 1000)
data = list(data1) + list(data2)
assert len(data) == 2000

_, bins, _ = plt.hist(data, bins=50, alpha=0.3, label='hist', density=True)
density = stats.gaussian_kde(data)
plt.plot(bins, density(bins), '--', label='Curve')
plt.legend()
plt.savefig('res.png')
plt.show()
