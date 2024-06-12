from ase.optimize import BFGS, QuasiNewton
from ase.constraints import FixAtoms
from ase.io import write, read
from gpaw import GPAW, PW
from ase.vibrations import Vibrations

atoms=read("init.vasp",format="vasp")
c = FixAtoms(indices=[atom.index for atom in atoms if atom.symbol=="Cu"])
atoms.set_constraint(c)

calc = GPAW(mode="lcao",h=0.25,
            xc='PBE',
            kpts=(1,1,1),
            occupations={'name': 'fermi-dirac',
                         'width': 0.1},
            txt='scf.txt',
            )
atoms.calc = calc

opt = BFGS(atoms,trajectory='relax.traj',logfile="relax.log")
opt.run(fmax=0.05)
write("final.vasp",atoms,format="vasp")

vib_indices=[atom.index for atom in atoms if atom.symbol in ["C","O"]]
vib = Vibrations(atoms,indices=vib_indices)
vib.run()
vib.summary()

vib.write_mode()

