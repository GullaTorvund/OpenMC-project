import matplotlib.pyplot as plt 
import openmc

"""
Making an ESFR pin cell
- still on R&D level
- based on knowledge from Superphenix (1985-1997)
"""

############################################
############## MATERIALS ###################
############################################


u235 = openmc.Material(name='U235')
u235.add_nuclide('U235', 1.0)
u235.set_density('g/cm3', 10.0)

u238 = openmc.Material(name='U238')
u238.add_nuclide('U238', 1.0)
u238.set_density('g/cm3', 10.0)

pu238 = openmc.Material(name='Pu238')
pu238.add_nuclide('Pu238', 1.0)
pu238.set_density('g/cm3', 10.0)

pu239 = openmc.Material(name='U235')
pu239.add_nuclide('Pu239', 1.0)
pu239.set_density('g/cm3', 10.0)

pu240 = openmc.Material(name='Pu240')
pu240.add_nuclide('Pu240', 1.0)
pu240.set_density('g/cm3', 10.0)

pu241 = openmc.Material(name='Pu241')
pu241.add_nuclide('Pu241', 1.0)
pu241.set_density('g/cm3', 10.0)

pu242 = openmc.Material(name='Pu242')
pu242.add_nuclide('Pu242', 1.0)
pu242.set_density('g/cm3', 10.0)

am241 = openmc.Material(name='Am241')
am241.add_nuclide('Am241', 1.0)
am241.set_density('g/cm3', 10.0)

o16 = openmc.Material(name='O16')
o16.add_nuclide('O16', 1.0)
o16.set_density('g/cm3', 10.0)

sodium = openmc.Material(name='Na')
sodium.add_nuclide('Na23', 1.0)
sodium.set_density('g/cm3', 0.96)

cu63 = openmc.Material(name='Cu63')
cu63.set_density('g/cm3', 10.0)
cu63.add_nuclide('Cu63', 1.0)

Al2O3 = openmc.Material(name='Al2O3')
Al2O3.set_density('g/cm3', 10.0)
Al2O3.add_element('O', 3.0)
Al2O3.add_element('Al', 2.0)

depl_U = openmc.Material(name='depleted U')
depl_U.add_element('U', 1.0, enrichment=0.5)
depl_U.add_element('O', 2.0)
depl_U.set_density('g/cm3', 10.97) #from wiki and nuclear-power.com

EM10 = openmc.Material(name='EM10 steel')
EM10.add_element('C', 0.099)
EM10.add_element('Ni', 0.07)
EM10.add_element('Cr', 8.97)
EM10.add_element('Cu', 0.05)
EM10.add_element('Si', 0.46)
EM10.add_element('Co', 0.03)
EM10.add_element('V', 0.013)
EM10.set_density('g/cm3', 10.0)

follower = openmc.Material(name='follower material')
follower.add_nuclide('Na23', 0.92)
follower.add_element('Fe', 0.0798)
follower.add_element('Mn', 0.0001)
follower.add_element('C', 0.0001)
follower.set_density('g/cm3', 10.0)

helium = openmc.Material(name='He')
helium.add_nuclide('He4', 1.0)
helium.set_density('g/cm3', 0.0001786)

boron_carbide = openmc.Material(name='boron carbide')
boron_carbide.add_element('B', 0.85)
boron_carbide.add_element('C', 0.15)
boron_carbide.set_density('g/cm3', 2.5)

# Material mixtures

inner_fuel = openmc.Material.mix_materials(
    [u235, u238, pu238, pu239, pu240, pu241, pu242, am241, o16],
    [0.0019, 0.7509, 0.0046, 0.0612, 0.0383, 0.0106, 0.0134, 0.001, 0.1181],
    'wo')

outer_fuel = openmc.Material.mix_materials(
    [u235, u238, pu238, pu239, pu240, pu241, pu242, am241, o16],
    [0.0018, 0.73, 0.0053, 0.0711, 0.0445, 0.0124, 0.0156, 0.0017, 0.1176],
    'wo')

# cladding: ODS steel (Oxide dispersion strengthened alloys)
clad_mat = openmc.Material.mix_materials(
    [cu63,Al2O3], [0.997,0.003], 'wo')








