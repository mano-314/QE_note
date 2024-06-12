from ase.io import read , write 
from ase.build import molecule 
import numpy as np 

h2o=molecule("H2O")
co2=molecule("CO2")
c6h6=molecule("C6H6")
hcooh=molecule("HCOOH")

cell=np.identity(3)*10
h2o.set_cell(cell)
co2.set_cell(cell)
c6h6.set_cell(cell)

write("h2o.vasp",h2o,format="vasp")
write("co2.cif",co2,format="cif")
write("c6h6.pwi",c6h6,format="espresso-in")
write("hcooh.com",hcooh,format="gaussian-in")

