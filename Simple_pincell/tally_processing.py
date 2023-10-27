import matplotlib.pyplot as plt 
import openmc
import numpy as np 

# Load the statepoint file
sp = openmc.StatePoint('statepoint.100.h5')


"""plotting spatial distribution of 
prompt neutron production"""

tally_pn = sp.get_tally(scores=['prompt-nu-fission'])
prompt_n = tally_pn.get_slice(scores=['prompt-nu-fission'])
prompt_n.mean.shape = (1000, 1000)

fig = plt.subplot(111)
imshow = fig.imshow(prompt_n.mean)
plt.colorbar(imshow)
plt.xlabel('x-grid') 
plt.ylabel('y-grid')
plt.title('Spatial distribution of prompt neutron production sites.')
plt.show()


"""plotting energy distribution of neutrons"""

tally_nf = sp.get_tally(scores=['flux'])
flux = tally_nf.get_slice(scores=['flux'])
flux_id = sp.tallies[tally_nf.id]
fluxmean = flux_id.mean.ravel()

energies = np.logspace(np.log10(1e-5), np.log10(20e6), 500)

plt.loglog(energies, fluxmean, color='forestgreen')
plt.xlabel('Energy (eV)') 
plt.ylabel('Flux intensity (neutrons per cm per source particle)')
plt.title('Energy distribution of neutron flux')
plt.show()


