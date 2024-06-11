from ase.calculators.espresso import Espresso, EspressoProfile
from ase.io import read, write
from ase.vibrations import Vibrations
from ase.constraints import FixAtoms
from ase.thermochemistry import HarmonicThermo, IdealGasThermo
import numpy as np
from ase.build import molecule 
from ase.optimize import BFGS


# -------------------------------------------------- general setting for DFT in calculator

pseudopotentials_dir = "../../pseudo"
pseudopotentials = {"H" : "h_pbe_v1.4.uspp.F.UPF",
                    "O" : "o_pbe_v1.2.uspp.F.UPF" }

profile = EspressoProfile(
    command='mpirun -n 16 pw.x', pseudo_dir=pseudopotentials_dir
)

control = dict(
    calculation = "scf",
    outdir      = "./output",
    prefix      = "opt",
    tprnfor     = True,
    )

system = dict(
    ibrav       = 0,
    ecutwfc     = 40,
    ecutrho     = 320.0,
    degauss     = 0.01,
    nspin       = 1,
    )

electrons=dict(
    conv_thr=1.E-8,
    mixing_beta=0.6,
    )

ions=dict(
    )

kpts=(1, 1, 1)
koffset=(0, 0, 0)


input_data = dict( control = control,
                   system = system,
                   electrons=electrons,
                   ions=ions  )

calc = Espresso( profile=profile,
                 input_data=input_data,
                 pseudopotentials=pseudopotentials,
                 # kpts=kpts,koffset=koffset 
               )

# -------------------------------------------------- pipline 

# 1) making atoms or importing atoms 
atoms=read("water.vasp",format="vasp")


# 2) set the calculator 
atoms.calc=calc


# 3) optimize the structure
opt = BFGS(atoms, trajectory='relax.traj', logfile='relax.log')
opt.run(fmax=0.01)
write("final_structure.vasp",atoms,format="vasp")


# 4) calculate the vibration 
vib = Vibrations(atoms)
vib.run()
vib.summary()
vib.write_mode()


# 5) calculate thermochemistry 
vib_energies = vib.get_energies()
vib_energies_real=vib_energies[np.isreal(vib_energies)]
thermo = IdealGasThermo(vib_energies=vib_energies_real,
                        potentialenergy=atoms.get_potential_energy(),
                        atoms=atoms,
                        geometry='nonlinear',
                        symmetrynumber=2, spin=0)
G = thermo.get_gibbs_energy(temperature=298.15, pressure=101325.)




