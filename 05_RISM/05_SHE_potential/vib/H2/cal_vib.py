from ase.io import read, write
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo, IdealGasThermo
import numpy as np

atoms=read("opt.vasp")
vib = Vibrations(atoms)
vib.run()
vib.summary()

vib_energies = vib.get_energies()
vib_energies_real=vib_energies[np.isreal(vib_energies)]
        
thermo = IdealGasThermo(vib_energies=vib_energies,
                        potentialenergy=0,
                        atoms=atoms,
                        geometry='linear', spin=0, 
                        symmetrynumber=2 )  # h2:2 , h2o:2 , h3o:3
G = thermo.get_gibbs_energy(temperature=298.15, pressure=101325.)


