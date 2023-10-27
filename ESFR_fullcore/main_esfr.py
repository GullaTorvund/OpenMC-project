import matplotlib.pyplot as plt 
import openmc
import openmc.deplete
import numpy as np 

from structure_esfr import core_r, FA_height, geometry, fuel_outer_d, clad_outer_d, crod_insertion_length, geometry

from matter_esfr import inner_fuel, outer_fuel, sodium, clad_mat, EM10, follower, boron_carbide

# calculating volume
n_iFA = 225
n_oFA = 228
n_iCSD = 6
n_oCSD = 18

n_pins_FA = 270
n_pins_CSD = 198
n_crods_CSD = 73

volume_innerfuel = ( n_iFA * n_pins_FA + n_iCSD * n_pins_CSD ) * FA_height * np.pi * fuel_outer_d
volume_outerfuel = ( n_oFA * n_pins_FA + n_oCSD * n_pins_CSD ) * FA_height * np.pi * fuel_outer_d
volume_crods     = ( n_iCSD + n_oCSD ) * n_crods_CSD * crod_insertion_length * np.pi * clad_outer_d

inner_fuel.volume = volume_innerfuel
outer_fuel.volume = volume_outerfuel
boron_carbide.volume = volume_crods


# exports
materials_file = openmc.Materials([inner_fuel, outer_fuel, sodium, clad_mat, EM10, follower, boron_carbide])
materials_file.export_to_xml()
geometry.export_to_xml()

##################################################
################### SETTINGS #####################
##################################################


#point = openmc.stats.Point((0,0,0))
#source = openmc.Source(space=point)

# specifing wanted statistics and runs


# creating initial uniform spatial source distribution over fissionable zones
x1 = core_r
y1 = x1
z1 = FA_height/2

bounds = [-x1, -y1, -z1, x1, y1, z1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], 
                                only_fissionable=True)

settings = openmc.Settings()
settings.batches = 100
settings.inactive = 10
settings.particles = 10000
settings.source = openmc.Source(space=uniform_dist)
settings.export_to_xml()


##################################################
################### TALLIES ######################
##################################################



####### NEUTRON FLUX #############################

"""
tallies_file = openmc.Tallies()

# Create mesh which will be used for tally
mesh = openmc.RegularMesh()
mesh.dimension = [1000,1000]
mesh.lower_left = [-core_r, -core_r]
mesh.upper_right = [core_r, core_r]

mesh_filter = openmc.MeshFilter(mesh)

# Instantiate neutron flux tally with en energy filter
tally_nf = openmc.Tally(name="Neutron flux")
tally_nf.filters = [mesh_filter]
tally_nf.scores = ['flux']
tallies_file.append(tally_nf)

tally_pn = openmc.Tally(name="prompt n")
tally_pn.filters = [mesh_filter]
tally_pn.scores = ['prompt-nu-fission']
tallies_file.append(tally_pn)

tallies_file.export_to_xml()
"""
openmc.run()

########### DEPLETION ############################


"""
themodel = openmc.model.Model()
themodel.geometry = geometry
themodel.settings = settings
themodel.materials = materials_file 

# ENDF/B-VII.1 Chain (Fast Spectrum)
path = '/Volumes/T7/nndc/chain_endfb71_sfr.xml'
chain = openmc.deplete.Chain.from_xml(path)
operator = openmc.deplete.CoupledOperator(themodel, path)

#power = 1200e6 # W 

# ESFR made to be 3600 MWth
power = 3600e6 # W 


# six months with time step of a month
time_steps = [30*24*60*60] * 6
integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power)

if __name__ == '__main__':
    integrator.integrate()

"""


