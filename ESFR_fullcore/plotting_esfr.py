import matplotlib.pyplot as plt 
import openmc
import numpy as np 

from structure_esfr import geometry
from matter_esfr import inner_fuel, outer_fuel, sodium, clad_mat

colordef = {inner_fuel: 'yellow', 
			outer_fuel: 'green', 
			sodium: 'red', 
			clad_mat: 'grey', }
"""
plot_xy = openmc.Plot.from_geometry(geometry)
plot_xy.color_by = 'material'
plot_xy.basis = 'xy'
plot_xy.origin = (0,0,0)

plot_xy.pixels = [800,800]
plot_xy.colors = colordef

plot_xz = openmc.Plot.from_geometry(geometry)
plot_xz.color_by = 'material'
plot_xz.basis = 'xz'

plot_xz.pixels = [1000,1000]
plot_xz.colors = colordef


plots = openmc.Plots([plot_xy, plot_xz])
"""


plots.export_to_xml()

openmc.plot_geometry()