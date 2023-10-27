import matplotlib.pyplot as plt 
import openmc
import numpy as np 

from matter_esfr import inner_fuel, outer_fuel, sodium, clad_mat, EM10, follower, boron_carbide


#############################################################################################
######### ---------------  REGIONS --------------------- ####################################
#############################################################################################

# lengths of pins
fuel_outer_d    = 0.943   # r = 0.4715  cm
clad_inner_d    = 0.973   # r = 0.4865  cm
clad_outer_d    = 1.073   # r = 0.5365  cm
edge_len_hexpin = 1.35    # calculated from hexagonal edges etc (edge_length = 2/sqrt(3) * r)

# lenghts of assemblies/core
lattice_pitch = 21.08        # cm, fuel assembly pitch
lattice_edge_len = 12.1706   # cm, lattice_pitch / sqrt(3)
core_r = 380                 # cm, radius of core including reflectors and extra sodium around
FA_height = 100 			 # cm, height of fuel rods/assemblies
h_top_ar = 70                # cm, height of axial reflector (top)
h_bottom_ar = 30             # cm, height of axial reflector (bottom)
crod_insertion_length = 30   # cm, how far the contron rods are inserted into the core

# all zplanes
ar_top = openmc.ZPlane(z0=+( FA_height/2+h_top_ar ), boundary_type='vacuum')                        # axial reflector (top)
ar_bottom = openmc.ZPlane(z0=-( FA_height/2+h_bottom_ar ), boundary_type='vacuum') 					# axial reflector (bottom)
FA_top = openmc.ZPlane(z0=+FA_height/2, boundary_type='transmission')								# fuel assemblies (top) 
FA_bottom = openmc.ZPlane(z0=-FA_height/2, boundary_type='transmission') 							# fuel assemblies (bottom)
crod_lower = openmc.ZPlane(z0=+(FA_height/2-crod_insertion_length), boundary_type='transmission')   # bottom cut of control rods (equivalent to upper plane of followers)

# (infinite) cylinder planes of pin cell geometry
fuel_outer_r = openmc.ZCylinder(r=fuel_outer_d/2, boundary_type='transmission')
clad_inner_r = openmc.ZCylinder(r=clad_inner_d/2, boundary_type='transmission')
clad_outer_r = openmc.ZCylinder(r=clad_outer_d/2, boundary_type='transmission')

# (infinite) hexagonal prism planes of pin, assembly and core
pin_outer_r  = openmc.model.hexagonal_prism(edge_length=edge_len_hexpin, orientation='y', boundary_type='transmission')
FA_outer_r = openmc.model.hexagonal_prism(edge_length=lattice_edge_len, orientation='x', boundary_type='transmission')
core_outer_r = openmc.model.hexagonal_prism(edge_length=core_r, orientation='y', boundary_type='vacuum')

# regions: pin cell
fuel_region = -FA_top & +FA_bottom & -fuel_outer_r					 # normal fuel pin
gap_region = -FA_top & +FA_bottom & +fuel_outer_r & -clad_inner_r    # fue-clad-gap
clad_region = -FA_top & +FA_bottom & +clad_inner_r & -clad_outer_r   # cladding
coolant_region = -FA_top & +FA_bottom & +clad_outer_r & pin_outer_r  # coolant filling fuel pin outside cladding
solid_pin_region = -FA_top & +FA_bottom & -clad_outer_r              # a "solid" pin of outer radius equal to cladding radius
wholepin_region = -FA_top & +FA_bottom & pin_outer_r                 # whole pin cell

# regions: control rods and follower
crod_main_region = -FA_top & +crod_lower & -clad_outer_r             # control rod region dependent on insertion length
crod_follower_region = -crod_lower & +FA_bottom & -clad_outer_r      # follower filling rest of FA height that is not control rod

# regions: assembly/core
FA_region = -FA_top & +FA_bottom & FA_outer_r      			# fuel assembly region
outercore_region = -FA_top & +FA_bottom & core_outer_r      # the core region inclusive radial reflectors, exclusive axial reflectors
upper_ar_region = -ar_top & + FA_top & core_outer_r         # upper axial reflector 
lower_ar_region = +ar_bottom & -FA_bottom & core_outer_r    # lower axial reflector 




#############################################################################################
######### --------------- PIN CELLS --------------------- ###################################
#############################################################################################


###### INNER FUEL ##########################

inner_fuel_cell = openmc.Cell(name='inner fuel')
inner_fuel_cell.fill = inner_fuel
inner_fuel_cell.region = fuel_region

inner_gap = openmc.Cell(name='sodium bond')
inner_gap.fill = sodium
inner_gap.region = gap_region

inner_clad = openmc.Cell(name='clad')
inner_clad.fill = clad_mat
inner_clad.region = clad_region

inner_coolant = openmc.Cell(name='coolant')
inner_coolant.fill = sodium
inner_coolant.region = coolant_region

innerfuel_uni = openmc.Universe(cells=(inner_fuel_cell, inner_gap, inner_clad, inner_coolant))


###### OUTER FUEL ##########################

outer_fuel_cell = openmc.Cell(name='outer fuel')
outer_fuel_cell.fill = outer_fuel
outer_fuel_cell.region = fuel_region

outer_gap = openmc.Cell(name='sodium bond')
outer_gap.fill = sodium
outer_gap.region = gap_region

outer_clad = openmc.Cell(name='clad')
outer_clad.fill = clad_mat
outer_clad.region = clad_region

outer_coolant = openmc.Cell(name='coolant')
outer_coolant.fill = sodium
outer_coolant.region = coolant_region

outerfuel_uni = openmc.Universe(cells=(outer_fuel_cell, outer_gap, outer_clad, outer_coolant))


###### RADIAL REFLECTOR ##########################

radref_cell = openmc.Cell(name='radial reflector')
radref_cell.fill = EM10
radref_cell.region = solid_pin_region

radref_coolant = openmc.Cell(name='coolant')
radref_coolant.fill = sodium
radref_coolant.region = coolant_region

radref_uni = openmc.Universe(cells=(radref_cell, radref_coolant))


###### ONLY SODIUM ########################

# sodium filled pin cell
single_sodium_cell = openmc.Cell(name='sodium cell')
single_sodium_cell.fill = sodium
single_sodium_cell.region = wholepin_region 

single_sodium_uni= openmc.Universe(cells=[single_sodium_cell])


###### FOLLOWER ########################

follower_cell = openmc.Cell(name='follower cell')
follower_cell.fill = follower
follower_cell.region = solid_pin_region

follower_coolent = openmc.Cell(name='coolant')
follower_coolent.fill = sodium
follower_coolent.region = coolant_region

follower_uni = openmc.Universe(cells=[follower_cell, follower_coolent])


###### CONTROL ROD ########################

crod_main_cell = openmc.Cell(name='contol rod cell')
crod_main_cell.fill = boron_carbide
crod_main_cell.region = crod_main_region

crod_follower_cell = openmc.Cell(name='contol rod follower cell')
crod_follower_cell.fill = follower
crod_follower_cell.region = crod_follower_region

crod_coolent = openmc.Cell(name='coolant')
crod_coolent.fill = sodium
crod_coolent.region = coolant_region

crod_uni = openmc.Universe(cells=[crod_main_cell,crod_follower_cell, crod_coolent])


##### AXIAL REFLECTORS  ##################

ar_upper_cell = openmc.Cell(name='upper axial reflector cell')
ar_upper_cell.fill = EM10
ar_upper_cell.region = upper_ar_region
ar_upper_uni = openmc.Universe(cells=[ar_upper_cell])

ar_lower_cell = openmc.Cell(name='lower axial reflector cell')
ar_lower_cell.fill = EM10
ar_lower_cell.region = lower_ar_region
ar_lower_uni = openmc.Universe(cells=[ar_lower_cell])



#############################################################################################
######### --------------- ASSEMBLIES --------------------- ##################################
#############################################################################################

def standardFA(fuel_uni, center_uni):
	"""standard fuel assembly in this reactor core"""
	array = np.array([ [fuel_uni]*54,
					   [fuel_uni]*48,
					   [fuel_uni]*42,
					   [fuel_uni]*36,
					   [fuel_uni]*30,
					   [fuel_uni]*24,
					   [fuel_uni]*18,
					   [fuel_uni]*12,
					   [fuel_uni]*6,
					   [center_uni]], dtype=openmc.Universe)

	return array

def crod_array(fuel_uni, other_uni):
	"""Assembly containing control rods"""
	ring3 = []; ring4 = []; ring5 = []; ring6 = []
	ring7 = []; ring8 = []; ring9 = []; ring10 = []

	for i in range(6):
		ring3  += [fuel_uni]   + [other_uni]
		ring4  += [other_uni]  + [fuel_uni]*2
		ring5  += [fuel_uni]*2 + [other_uni]  + [fuel_uni]
		ring6  += [fuel_uni]   + [other_uni]  + [fuel_uni]*2 + [other_uni] 
		ring7  += [other_uni]  + [fuel_uni]*2 + [other_uni]  + [fuel_uni]*2 
		ring8  += [fuel_uni]*2 + [other_uni]  + [fuel_uni]*2 + [other_uni]  + [fuel_uni] 
		ring9  += [other_uni]  + [fuel_uni]*7
		ring10 += [fuel_uni]*3 + [other_uni]  + [fuel_uni]*2 + [other_uni]  + [fuel_uni]*2

	ass_array = np.array([ ring10,
						   ring9,
						   ring8,
						   ring7,
						   ring6,
						   ring5,
						   ring4,
						   ring3,
						  [fuel_uni]*6,
						  [other_uni]], dtype=openmc.Universe)

	return ass_array

###### INNER FA ############################

iFA_sodium_cell = openmc.Cell(fill=sodium)
iFA_outer_universe = openmc.Universe(cells=[iFA_sodium_cell])

iFA_lat = openmc.HexLattice(name='inner FA')
iFA_lat.center = (0, 0)
iFA_lat.pitch = (lattice_pitch/17,)
iFA_lat.orientation = 'x'
iFA_lat.outer = iFA_outer_universe

iFA_lat.universes = standardFA(innerfuel_uni, single_sodium_uni)
iFA_cell  = openmc.Cell(fill=iFA_lat, region=FA_region)
iFA_uni = openmc.Universe(cells=[iFA_cell], name='inner FA universe')


###### OUTER FA ############################

oFA_sodium_cell = openmc.Cell(fill=sodium)
oFA_outer_universe = openmc.Universe(cells=[oFA_sodium_cell])

oFA_lat = openmc.HexLattice(name='inner FA')
oFA_lat.center = (0, 0)
oFA_lat.pitch = (lattice_pitch/17,)
oFA_lat.orientation = 'x'
oFA_lat.outer = oFA_outer_universe

oFA_lat.universes = standardFA(outerfuel_uni, single_sodium_uni)
oFA_cell = openmc.Cell(fill=oFA_lat, region=FA_region)
oFA_uni = openmc.Universe(cells=[oFA_cell])


###### RADIAL REFLECTOR ASSEMBLY ############################

radref_ass_sodium_cell = openmc.Cell(fill=sodium)
radref_ass_outer_universe = openmc.Universe(cells=[radref_ass_sodium_cell])

radref_ass_lat = openmc.HexLattice(name='radial reflector')
radref_ass_lat.center = (0, 0)
radref_ass_lat.pitch = (lattice_pitch/17,)
radref_ass_lat.orientation = 'x'
radref_ass_lat.outer = radref_ass_outer_universe

radref_ass_lat.universes = standardFA(radref_uni, radref_uni)
radref_ass_cell = openmc.Cell(fill=radref_ass_lat, region=FA_region)
radref_ass_uni = openmc.Universe(cells=[radref_ass_cell])


###### INNER CSD ASSEMBLY ############################
# Control Shutdown Devices in the inner fuel region

CSDinner_sodium_cell = openmc.Cell(fill=sodium)
CSDinner_outer_universe = openmc.Universe(cells=[CSDinner_sodium_cell])

CSDinner_lat = openmc.HexLattice(name='CSD')
CSDinner_lat.center = (0, 0)
CSDinner_lat.pitch = (lattice_pitch/17,)
CSDinner_lat.orientation = 'x'
CSDinner_lat.outer = CSDinner_outer_universe
CSDinner_lat.universes = crod_array(innerfuel_uni, crod_uni)

CSDinner_cell = openmc.Cell(fill=CSDinner_lat, region=FA_region)
CSDinner_ass_uni = openmc.Universe(cells=[CSDinner_cell])


###### OUTER CSD ASSEMBLY ############################
# Control Shutdown Devices in the outer fuel region

CSDouter_sodium_cell = openmc.Cell(fill=sodium)
CSDouter_outer_universe = openmc.Universe(cells=[CSDouter_sodium_cell])

CSDouter_lat = openmc.HexLattice(name='CSD')
CSDouter_lat.center = (0, 0)
CSDouter_lat.pitch = (lattice_pitch/17,)
CSDouter_lat.orientation = 'x'
CSDouter_lat.outer = CSDouter_outer_universe
CSDouter_lat.universes = crod_array(outerfuel_uni, crod_uni)

CSDouter_cell = openmc.Cell(fill=CSDouter_lat, region=FA_region)
CSDouter_ass_uni = openmc.Universe(cells=[CSDouter_cell])

###### DSD ASSEMBLY ############################
# Diverse Shutdown Devices in the inner fuel region

DSD_sodium_cell = openmc.Cell(fill=sodium)
DSD_outer_universe = openmc.Universe(cells=[DSD_sodium_cell])

DSD_lat = openmc.HexLattice(name='CSD')
DSD_lat.center = (0, 0)
DSD_lat.pitch = (lattice_pitch/17,)
DSD_lat.orientation = 'x'
DSD_lat.outer = DSD_outer_universe
DSD_lat.universes = crod_array(innerfuel_uni, follower_uni)

DSD_cell = openmc.Cell(fill=DSD_lat, region=FA_region)
DSD_ass_uni = openmc.Universe(cells=[DSD_cell])


#############################################################################################
######### --------------- FULL CORE --------------------- ###################################
#############################################################################################

# OUTER UNIVERSE (of sodium)
core_sodium_cell = openmc.Cell(fill=sodium)
core_outer_universe = openmc.Universe(cells=[core_sodium_cell])

core_lat = openmc.HexLattice(name='fullcore')
core_lat.center = (0, 0)
core_lat.pitch = (lattice_pitch,)
core_lat.orientation = 'y'
core_lat.outer = core_outer_universe


# mixed rings in core 
ring4 = []; ring7 = [iFA_uni]; ring10 = []; 
ring11 = []; ring13 = []; ring14 = []

for i in range(6):
	ring10 += [oFA_uni]*2 + [CSDouter_ass_uni] + [iFA_uni]*4 + [CSDouter_ass_uni] + [oFA_uni]
	ring4 += [CSDinner_ass_uni] + [iFA_uni]*2 
	ring11 += [oFA_uni]*5 + [CSDouter_ass_uni] + [oFA_uni]*4
	ring13 += [radref_ass_uni] + [oFA_uni]*11
	ring14 += [radref_ass_uni]*5 + [oFA_uni]*4 + [radref_ass_uni]*4

for i in range(8):
	ring7 += [DSD_ass_uni] + [iFA_uni]*3 
ring7 += [DSD_ass_uni] + [iFA_uni]*2 

core_uni_grid = np.array([ [radref_ass_uni]*96,
						   [radref_ass_uni]*90,
						   [radref_ass_uni]*84,
						   ring14,
						   ring13,
						   [oFA_uni]*66,
						   ring11,
						   ring10,
						   [iFA_uni]*48,
						   [iFA_uni]*42,
						   ring7,
						   [iFA_uni]*30,
						   [iFA_uni]*24,
						   ring4,
						   [iFA_uni]*12,
						   [iFA_uni]*6,
						   [radref_ass_uni] ], dtype=openmc.Universe)

core_lat.universes = core_uni_grid
core_cell = openmc.Cell(fill=core_lat, region=outercore_region)
core_uni = openmc.Universe(cells=[core_cell, ar_lower_cell, ar_upper_cell])

# export full core geometry
geometry = openmc.Geometry()
geometry.root_universe = core_uni 


#############################################################################################
######### --------------- PLOTTING --------------------- ####################################
#############################################################################################

colordef = {inner_fuel: 'darkmagenta', 
			outer_fuel: 'cyan', 
			sodium: 'darkorange', 
			clad_mat: 'grey', 
			EM10: 'forestgreen',
			follower: 'rosybrown',
			boron_carbide: 'firebrick'}

# iFA_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)
# oFA_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)
# radref_ass_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)

# CSDinner_ass_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)
# CSDinner_ass_uni.plot(origin = (0,0,0), basis='xz', pixels=(2000, 2000), width = (25.,100.), color_by = 'material', colors=colordef)
# CSDouter_ass_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)
# CSDouter_ass_uni.plot(origin = (0,0,0), basis='xz', pixels=(2000, 2000), width = (25.,100.), color_by = 'material', colors=colordef)
# DSD_ass_uni.plot(origin = (0,0,0), basis='xy', pixels=(2000, 2000), width = (25.,25.), color_by = 'material', colors=colordef)
# DSD_ass_uni.plot(origin = (0,0,0), basis='xz', pixels=(2000, 2000), width = (25.,100.), color_by = 'material', colors=colordef)


# core_uni.plot(origin = (0,0,0), basis='xy', pixels=(4000, 4000), width = (800.,800.), color_by = 'material', colors=colordef)
# core_uni.plot(origin = (0,0,0), basis='xz', pixels=(4000, 4000), width = (800.,230.), color_by = 'material', colors=colordef)

# plt.show()





"""
NoteS:

With depleted uranium as radial reflector, the reactor was barely critical (without any control)
Had to switch.

"""




