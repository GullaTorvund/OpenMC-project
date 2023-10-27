import matplotlib.pyplot as plt 
import openmc
import numpy as np 

"""
Goal: finding Thermal utilization factor (f) as function of fuel pin radius.

Prosedure:
- Load the statepoint file
- Get thermal absorption in all materials and in fuel only and calculate f
- Ad hoc solution: print f each time, add to flist in relation to the fuel radius used in simulation
- Plot results
"""

sp = openmc.StatePoint('statepoint.100.h5')
therm_abs_rate = sp.get_tally(name='therm. abs. rate')
fuel_therm_abs_rate = sp.get_tally(name='fuel therm. abs. rate')
f = fuel_therm_abs_rate / therm_abs_rate

#print(f.mean.ravel())


rlist = np.array([3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1, 5.3, 5.5, 5.7, 
			      5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7,
			      7.9, 8.1, 8.3, 8.5, 8.7, 8.9, 9.1, 9.3])

flist = np.array([0.52882093, 0.55097436, 0.57541746, 0.59844862, 
				  0.6180893, 0.63799292, 0.6581118, 0.67783823, 
				  0.69272166, 0.70954505, 0.72649378, 0.73898989,
				  0.75271872, 0.76799724, 0.78002196, 0.79361035,
				  0.80421575, 0.81623559, 0.82570428, 0.83616068,
				  0.84626827, 0.85614877, 0.86327389, 0.87166806,
				  0.88022704, 0.88778505, 0.89510806, 0.90178828])

plt.grid()
plt.scatter(rlist, flist, color='forestgreen')
plt.xlabel('Radius of pincell (mm)') 
plt.ylabel(r'Thermal utilization factor $f$')
plt.title(r'Thermal utilization factor $f$ as function of fuel pin radius')
plt.show()