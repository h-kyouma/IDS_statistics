#Konrad Clapa 
# Generates random numbers to simulate standard normal distribution with $i number of samples 
# Plots the normal disribution
# Calaculates the cumulative distribution
# Plots the cumulative density distribution

import matplotlib.pyplot as plt
import numpy as np

#numer of samples
i = 10000

#bins in the range
bins = 50
#density
density = 1 

#generate numbers
data = np.random.randn(i)



hx, hy, _ = plt.hist(data, bins=bins, density=density , color="yellow")

plt.ylim(0.0,max(hx)+0.11)
plt.title('This is the standard distribution for {} samples'.format(i))
plt.grid()
plt.savefig("cdd_001.png", bbox_inches='tight')

#Uncomment the bellow to see the plot
plt.show()
#plt.close()

dx = hy[1] - hy[0]
f = np.cumsum(hx)*dx

plt.plot(hy[1:], f)
plt.title('This is the cumulative distribution function CDF')
plt.savefig("cdd_02.png", bbox_inches='tight')
plt.show()
#plt.close()
