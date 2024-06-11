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
    calculation = "relax",
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


# 3) control ase to do static calculation but relax in QE loop
atoms.get_potential_energy()

atoms_opt=read("espresso.pwo",index=-1)
write("final_structure.vasp",atoms_opt,format="vasp")




