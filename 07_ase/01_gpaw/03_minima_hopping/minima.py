from ase.optimize import BFGS
from ase.constraints import FixAtoms
from ase.io import write, read
from ase.optimize.minimahopping import MinimaHopping, MHPlot
from gpaw import GPAW, PW

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

hop = MinimaHopping(atoms,
                    Ediff0=0.5,
                    T0=300.0,
                    fmax=0.05 )
hop(totalsteps=10)
mhplot = MHPlot()
mhplot.save_figure('summary.png')


write("CONTCAR",atoms,format="vasp")



