import matplotlib.pyplot as plt 
import openmc
import numpy as np 

###################################################################
######### ---------------  MATERIALS ---------------- #############
###################################################################

uo2 = openmc.Material(name='uo2')
uo2.add_element('U', 1.0, enrichment=2.0) 
uo2.add_element('O', 2.0)
uo2.set_density('g/cm3', 10.97) #from wiki and nuclear-power.com

water = openmc.Material(name='h2o')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 1.0)
water.add_s_alpha_beta('c_H_in_H2O') # use xs for H in h2o

heavy_water = openmc.Material(name='heavy water')
heavy_water.add_nuclide('H2', 2.0)
heavy_water.add_nuclide('O16', 1.0)
heavy_water.add_s_alpha_beta('c_D_in_D2O')
heavy_water.set_density('g/cm3', 1.1)

helium = openmc.Material(name='He')
helium.add_nuclide('He4', 1.0)
helium.set_density('g/cm3', 0.0001786)

zircaloy4 = openmc.Material(name='zircaloy4')
zircaloy4.add_element('Zr', 0.985)
zircaloy4.add_element('Sn', 0.014)
zircaloy4.add_element('O',  0.0012)
zircaloy4.add_element('Fe', 0.0020)
zircaloy4.add_element('Cr', 0.0010)
zircaloy4.set_density('g/cm3', 6.56)

materials = openmc.Materials([uo2, zircaloy4, water, heavy_water, helium])
materials.export_to_xml()

###################################################################
######### ---------------  REGIONS ---------------- ###############
###################################################################

pitch_width   = 1.4  # cm
pitch_height  = 2.0  # cm
fuel_radius   = 0.4  # cm, try 0.2 and switch between light and heavy water moderator 
clad_i_radius = 0.42 # cm, try 0.22 and switch between light and heavy water moderator
clad_o_radius = 0.45 # cm, try 0.25 and switch between light and heavy water moderator


fuel_outer_r = openmc.ZCylinder(r=fuel_radius)   
clad_inner_r = openmc.ZCylinder(r=clad_i_radius) 
clad_outer_r = openmc.ZCylinder(r=clad_o_radius) 

# analysis: change between vacuum and reflective boundary conditions
box = openmc.rectangular_prism(width=pitch_width, height=pitch_width,
                               boundary_type='reflective')
top = openmc.ZPlane(z0=+pitch_height/2, boundary_type='reflective')                  
bottom = openmc.ZPlane(z0=-pitch_height/2, boundary_type='reflective')   

fuel_region = -fuel_outer_r & +bottom & -top
gap_region = +fuel_outer_r & -clad_inner_r & +bottom & -top
clad_region = +clad_inner_r & -clad_outer_r & +bottom & -top
water_region = box & +clad_outer_r & +bottom & -top

###################################################################
######### ------------  CELLS + UNIVERSE -------------- ###########
###################################################################

fuel = openmc.Cell(name='fuel')
fuel.fill = uo2
fuel.region = fuel_region

gap = openmc.Cell(name='air gap')
gap.fill = helium
gap.region = gap_region

clad = openmc.Cell(name='clad')
clad.fill = zircaloy4
clad.region = clad_region
                           
moderator = openmc.Cell(name='moderator')
moderator.fill = water 
moderator.region = water_region

#Assigning cells to universe
pincell_universe = openmc.Universe(cells=(fuel, gap, clad, moderator))

geometry = openmc.Geometry(pincell_universe)
geometry.export_to_xml()

###################################################################
####### --------------  PLOTTING PIN CELL --------------- #########
###################################################################


colordefs = {uo2: 'darkgreen', 
            helium: 'pink', 
            zircaloy4: 'black', 
            water: 'lightblue'}

plot_topview = openmc.Plot()
plot_topview.width = (pitch_width,pitch_width)
plot_topview.pixels = (1000,1000)
plot_topview.color_by = 'material'
plot_topview.colors = colordefs

plot_sideview = openmc.Plot()
plot_sideview.basis = 'xz'
plot_sideview.width = (pitch_width,pitch_height)
plot_sideview.pixels = (1000,1000)
plot_sideview.color_by = 'material'
plot_sideview.colors = colordefs

plots = openmc.Plots([plot_topview, plot_sideview])
plots.export_to_xml()

#running openmc in plotting mode
openmc.plot_geometry()

###################################################################
######### ---------------  RUNNING ---------------- ###############
###################################################################
"""
point = openmc.stats.Point((0,0,0))
source = openmc.Source(space=point)

# specifing wanted statistics and runs
settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 10
settings.particles = 1000

# creating initial uniform spatial source distribution over fissionable zones
x1 = fuel_radius/2
y1 = x1
z1 = pitch_height/2

bounds = [-x1, -y1, -z1, x1, y1, z1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], 
                                only_fissionable=True)
settings.source = openmc.Source(space=uniform_dist)
settings.export_to_xml()
"""
###################################################################
######### ---------------  TALLIES ---------------- ###############
###################################################################

"""
# need mesh filter for spacial distribution
mesh = openmc.RegularMesh()
mesh.dimension = [1000,1000]
mesh.lower_left = [-pitch_width/2, -pitch_width/2]
mesh.upper_right = [pitch_width/2, pitch_width/2]
mesh_filter = openmc.MeshFilter(mesh)

tallies = openmc.Tallies()


###### Wish to plot spacial distribution of prompt neutron production. ########

tally_pn = openmc.Tally(name="prompt n")
tally_pn.filters = [mesh_filter]
tally_pn.scores = ['prompt-nu-fission']
tallies.append(tally_pn)


###### Wish to plot the energy distribution of neutron flux. ########

# Create equal-lethargy energies to put in filter
energies = np.logspace(np.log10(1e-5), np.log10(20e6), 501)
e_filter = openmc.EnergyFilter(energies)

tally_nf = openmc.Tally(name="n flux")
tally_nf.filters = [e_filter, openmc.CellFilter([fuel])]
tally_nf.scores = ['flux']
tallies.append(tally_nf)

tallies.export_to_xml()
"""
#openmc.run()





"""
-------------------------------------------------------------------
Results with different parameters.
-------------------------------------------------------------------

k-value for LIGHT WATER (VACUUM):

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 0.00968 +/- 0.00013
 k-effective (Track-length)  = 0.00949 +/- 0.00005
 k-effective (Absorption)    = 0.00898 +/- 0.00049
 Combined k-effective        = 0.00950 +/- 0.00005
 Leakage Fraction            = 0.99578 +/- 0.00024



k-value for LIGHT WATER (REFLECTIVE):

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 1.29470 +/- 0.00423
 k-effective (Track-length)  = 1.28955 +/- 0.00514
 k-effective (Absorption)    = 1.29559 +/- 0.00375
 Combined k-effective        = 1.29484 +/- 0.00333
 Leakage Fraction            = 0.00000 +/- 0.00000



k-value for HEAVY WATER (REFLECTIVE):

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 0.87239 +/- 0.00401
 k-effective (Track-length)  = 0.87284 +/- 0.00450
 k-effective (Absorption)    = 0.86392 +/- 0.00368
 Combined k-effective        = 0.86743 +/- 0.00342
 Leakage Fraction            = 0.00000 +/- 0.00000


k-value for LIGHT WATER (REFLECTIVE), FUEL RADIUS 0.2:

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 0.89337 +/- 0.00280
 k-effective (Track-length)  = 0.89095 +/- 0.00360
 k-effective (Absorption)    = 0.89394 +/- 0.00328
 Combined k-effective        = 0.89321 +/- 0.00257
 Leakage Fraction            = 0.00000 +/- 0.00000


k-value for HEAVY WATER (REFLECTIVE), FUEL RADIUS 0.2:

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 1.33855 +/- 0.00448
 k-effective (Track-length)  = 1.33994 +/- 0.00554
 k-effective (Absorption)    = 1.33996 +/- 0.00334
 Combined k-effective        = 1.33977 +/- 0.00302
 Leakage Fraction            = 0.00000 +/- 0.00000

"""















