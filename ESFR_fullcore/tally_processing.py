import matplotlib.pyplot as plt 
import openmc
import numpy as np 

# Load the statepoint file
#sp = openmc.StatePoint('statepoint.100.h5')
sp = openmc.StatePoint('tallies10000particles.100.h5')

tally_nf = sp.get_tally(scores=['flux'])
flux = tally_nf.get_slice(scores=['flux'])
flux_id = sp.tallies[tally_nf.id]
flux_mean = flux_id.mean
flux_mean.shape = [1000,1000] 

fig = plt.subplot(111)
imshow = fig.imshow(flux_mean)
plt.colorbar(imshow)
plt.xlabel('x-grid')
plt.ylabel('y-grid')
plt.title('Neutron flux distribution in ESFR model')
plt.show()


tally_pn = sp.get_tally(scores=['prompt-nu-fission'])
prompt_n = tally_pn.get_slice(scores=['prompt-nu-fission'])
prompt_n.mean.shape = [1000,1000]

fig = plt.subplot(111)
imshow = fig.imshow(prompt_n.mean)
plt.colorbar(imshow)
plt.xlabel('x-grid')
plt.ylabel('y-grid')
plt.title('Prompt neutron production sites in ESFR model')
plt.show()

