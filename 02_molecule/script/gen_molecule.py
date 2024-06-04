from ase.io import write
from ase.build import molecule 
import sys 

molname=sys.argv[1]
mol=molecule(molname)
mol.set_cell([[10,0,0],[0,10,0],[0,0,10]])
mol.center()
write("{}.pwi".format(molname), mol , format="espresso-in")
