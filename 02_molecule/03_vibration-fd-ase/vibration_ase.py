from ase.calculators.espresso import Espresso, EspressoProfile
from ase.io.espresso import write_espresso_in
from ase.io import read, write
from ase.vibrations import Vibrations
from ase.constraints import FixAtoms
from ase.thermochemistry import HarmonicThermo, IdealGasThermo
import sys
import numpy as np

argv=sys.argv[1:]
input_structure=argv[0]

# -------------------------------------------------- general setting

pseudopotentials_dir = "../../pseudo"

pseudopotentials = {'Cu': 'cu_pbe_v1.2.uspp.F.UPF',
                    "H" : "h_pbe_v1.4.uspp.F.UPF",
                    "C" : "c_pbe_v1.2.uspp.F.UPF",
                    'N' : 'n_pbe_v1.2.uspp.F.UPF',
                    'O' : 'o_pbe_v1.2.uspp.F.UPF',
                    }

profile = EspressoProfile(
    command='mpirun -n 16 pw.x', pseudo_dir=pseudopotentials_dir
)

# -------------------------------------------------- DFT input

control = dict(
    calculation = "scf",
    pseudo_dir  = pseudopotentials_dir,
    outdir      = "./output",
    prefix      = "opt",
    tprnfor     = True,
    )

system = dict(
    ibrav       = 0,
    ecutwfc     = 40,
    ecutrho     = 320.0,
    occupations = "smearing",
    smearing    = "gauss",
    degauss     = 0.01,
    nspin       = 1,
    nosym       = True,
    )

electrons=dict(
    electron_maxstep=200,
    conv_thr=1.E-8,
    mixing_beta=0.6,
    # diagonalization='rmm-davidson',
    # startingwfc='file',
    )

ions=dict(
    upscale=1,
    )

kpts=(1, 1, 1)
koffset=(0, 0, 0)

# --------------------------------------------reading and setting DFT

# reading structure
atoms=read(input_structure)
atomic_species=[]
for atom in atoms :
    if atom.symbol not in atomic_species:
        atomic_species.append(atom.symbol)
print( "atomic species found : ",atomic_species)

# set intput parameters
print("creating input")
input_data = dict(
            control = control,
            system = system,
            electrons=electrons,
            ions=ions,
        )
additional_cards=False

# set calculator
calc = Espresso(profile=profile,
                input_data=input_data,
                pseudopotentials=pseudopotentials,
                additional_cards=additional_cards,
#                kpts=kpts,koffset=koffset
                )
atoms.calc=calc

# --------------------------------------------creating

print("performing vibration mode")

vib = Vibrations(atoms)
vib.run()
vib.summary()
vib.write_mode()

vib_energies = vib.get_energies()
vib_energies_real=vib_energies[np.isreal(vib_energies)]

# ------------- adsorbate 
#thermo = HarmonicThermo(vib_energies=vib_energies_real,
#                potentialenergy=0.0)
#entro = thermo.get_entropy(temperature=298.15, verbose=True)
#inter = thermo.get_internal_energy(temperature=298.15, verbose=True)

# ------------- free gas
thermo = IdealGasThermo(vib_energies=vib_energies_real,
                        potentialenergy=0.0,
                        atoms=atoms,
                        geometry='nonlinear',
                        symmetrynumber=2, spin=0)
G = thermo.get_gibbs_energy(temperature=298.15, pressure=101325.)





