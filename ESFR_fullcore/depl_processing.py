import matplotlib.pyplot as plt 
import openmc
import openmc.deplete
import numpy as np 

"""Take a look at changes of keff over time"""
results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")
# time, k = results.get_eigenvalue()
# time /= (24*60*60)  # convert back to days from seconds

# plt.errorbar(time, k[:, 0], yerr=k[:, 1], color='forestgreen', fmt='-o', linestyle='--', linewidth=2)
# plt.xlabel("Time [d]")
# plt.ylabel(r'$k_{eff}\pm \sigma$')
# plt.ylim([0.998,1.01])
# plt.title(r'Evolution of $k_{eff}$ during six months')
# plt.grid()
# plt.show()


"""Take a look at conversion ratio of 235U vs 239Pu"""
t, U5_i = results.get_atoms(mat = "18",nuc = "U235")
t, Pu9_i = results.get_atoms(mat = "18",nuc = "Pu239")

t, U5_o = results.get_atoms(mat = "19",nuc = "U235")
t, Pu9_o = results.get_atoms(mat = "19",nuc = "Pu239")

U5_tot = U5_i + U5_o
Pu9_tot = Pu9_i + Pu9_o

con_ratio = Pu9_tot/U5_tot
t /= (24*60*60)

#plt.plot(t, Pu9_tot, label = "239Pu")
#plt.plot(t, U5_tot, label = "235U")

plt.plot(t, con_ratio, color='forestgreen', linewidth=2.5, linestyle='--',)
plt.xlabel("Time [d]")
plt.ylabel(r'$\frac{N_{239Pu}}{N_{235U}}$');
plt.title("Conversion ratio of 239Pu vs 235U")
plt.grid()
plt.show()