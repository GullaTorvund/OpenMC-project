import matplotlib.pyplot as plt 
import openmc
import numpy as np 

###################################################################
######### ---------------  MATERIALS ---------------- #############
###################################################################

uo2 = openmc.Material(name='uo2')
uo2.add_element('U', 1.0, enrichment=3.2) # changed from enrichment=2.0
uo2.add_element('O', 2.0)
uo2.set_density('g/cm3', 10.97) 

water_borated = openmc.Material(name='h2o')
water_borated.add_nuclide('H1', 2.0)
water_borated.add_nuclide('O16', 1.0)
water_borated.add_element('B', 0.000343) # 0.00033 works
water_borated.set_density('g/cm3', 1.0)
water_borated.add_s_alpha_beta('c_H_in_H2O') # use xs for H in h2o

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

materials = openmc.Materials([uo2, zircaloy4, water_borated, helium])
materials.export_to_xml()

###################################################################
######### ---------------  REGIONS ---------------- ###############
###################################################################

# thermal neutron diffusion length is 2.54 cm
pitch_width = 2.54  # cm
pitch_height = 3.0  # cm
fuel_radius  = 0.41 # cm

# typical pin cell size on PWR
fuel_outer_r = openmc.ZCylinder(r=fuel_radius)
clad_inner_r = openmc.ZCylinder(r=0.43)          
clad_outer_r = openmc.ZCylinder(r=0.49)          

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
moderator.fill = water_borated
moderator.region = water_region

#Assigning cells to universe
pincell_universe = openmc.Universe(cells=(fuel, gap, clad, moderator))

geometry = openmc.Geometry(pincell_universe)
geometry.export_to_xml()

###################################################################
######### ---------------  RUNNING ---------------- ###############
###################################################################

point = openmc.stats.Point((0,0,0))
source = openmc.Source(space=point)

# specifing wanted statistics and runs
settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 10
settings.particles = 10000

# creating initial uniform spatial source distribution over fissionable zones
x1 = fuel_radius/2
y1 = x1
z1 = pitch_height/2

bounds = [-x1, -y1, -z1, x1, y1, z1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], 
                                only_fissionable=True)
settings.source = openmc.Source(space=uniform_dist)
settings.export_to_xml()


###################################################################
######### ---------------  TALLIES ---------------- ###############
###################################################################


tallies = openmc.Tallies()
thermal_region = [0., 0.625]

# thermal absorption in all materials
therm_abs_rate = openmc.Tally(name='therm. abs. rate')
therm_abs_rate.scores = ['absorption']
therm_abs_rate.filters = [openmc.EnergyFilter(thermal_region)]

tallies.append(therm_abs_rate)


# thermal absorption in fuel only
fuel_therm_abs_rate = openmc.Tally(name='fuel therm. abs. rate')
fuel_therm_abs_rate.scores = ['absorption']
fuel_therm_abs_rate.filters = [openmc.EnergyFilter(thermal_region),
                               openmc.CellFilter([fuel])]

tallies.append(fuel_therm_abs_rate)

tallies.export_to_xml()

openmc.run()



###################################################################
######### ---------------  PLOTTING ---------------- ##############
###################################################################

"""
#plotting topview
plot_topview = openmc.Plot()
plt.filename = 'pinplot_topview'
plot_topview.width = (pitch_width,pitch_width)
plot_topview.pixels = (400,400)
plot_topview.color_by = 'material'
plot_topview.colors = {uo2: 'yellow', helium: 'white', zircaloy4: 'grey', water: 'blue'}


plots = openmc.Plots([plot_topview])
plots.export_to_xml()

#running openmc in plotting mode
openmc.plot_geometry()
"""


"""
What did I do?

Optimilized box pitch (increased it) to fit average thermal neutron diffusion
Put some boron to absorb more neutrons
Increased enrichment

Results from the run:

 ============================>     RESULTS     <============================

 k-effective (Collision)     = 0.99901 +/- 0.00113
 k-effective (Track-length)  = 0.99835 +/- 0.00137
 k-effective (Absorption)    = 1.00098 +/- 0.00109
 Combined k-effective        = 1.00001 +/- 0.00089
 Leakage Fraction            = 0.00000 +/- 0.00000

"""



