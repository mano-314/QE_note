from ase.calculators.espresso import Espresso
from ase.io.espresso import write_espresso_in
from ase.io import read, write
from ase.vibrations import Vibrations
from ase.constraints import FixAtoms
from ase.thermochemistry import HarmonicThermo
import sys
import numpy as np
argv=sys.argv[1:]
input_structure=argv[0]

# -------------------------------------------------- select mode

run_mode       = True
geninput_mode  = False

relax_mode     = True
scf_mode       = False
vibration_mode = False

set_constraint = True

trism          = False
lfcp           = False
charge         = 0.0

# -------------------------------------------------- general setting for DFT 

pseudopotentials_dir = "/project/lt200240-ccoxrr/mano/02_for_rism/pseudo"


pseudopotentials = {'Cu': 'cu_pbe_v1.2.uspp.F.UPF',
                    "H" : "h_pbe_v1.4.uspp.F.UPF",
                    "C" : "c_pbe_v1.2.uspp.F.UPF",
                    'N' : 'n_pbe_v1.2.uspp.F.UPF',
                    'O' : 'o_pbe_v1.2.uspp.F.UPF',
                    }

additional_cards = ["SOLVENTS {mol/L}",
                    "H2O -1.0 H2O.tip5p.Nishihara.MOL",
                    "H3O+ 1.0 H3O+.Bonthuls.Nishihara.MOL",
                    "NO3- 1.0 NO3-.Anagnostopoulos.MOL" ]

lj_parameter_database={
    "Cu":{"epsilon":0.05,   "sigma":3.60},
    "H" :{"epsilon":0.046,  "sigma":1.00},
    "C" :{"epsilon":0.07,   "sigma":3.55},
    "N" :{"epsilon":0.17,   "sigma":3.25},
    "O" :{"epsilon":0.1554, "sigma":3.166}
}


if relax_mode:
    calculation_tag="relax"
if scf_mode:
    calculation_tag="scf"
if vibration_mode:
    calculation_tag="scf"

if geninput_mode:
    outfilename="scf.in"


control = dict(
    calculation = calculation_tag,
    pseudo_dir  = pseudopotentials_dir,
    outdir      = "./output",
    prefix      = "opt",
    tprnfor     = True,
    trism       = trism,
    lfcp        = lfcp,
    nstep       = 200,
    etot_conv_thr = 1.0E-5,
    forc_conv_thr = 1.0E-4,
    )

system = dict(
    ibrav       = 0,
    ecutwfc     = 20,
    ecutrho     = 160.0,
    occupations = "smearing",
    smearing    = "gauss",
    degauss     = 0.01,
    nspin       = 1,
    input_dft   = "vdw-df2-b86r",
    nosym       = True,
    )

system_update=dict(
    assume_isolated = "esm",
    esm_bc = "bc1",
    tot_charge = charge,
)

electrons=dict(
    electron_maxstep=200,
    conv_thr=1.E-6,
    mixing_beta=0.1,
    diagonalization='david',
    )

ions=dict(
    upscale=1,
    )

fcp =dict(
    fcp_mu           = -5.0,
    fcp_dynamics     = "bfgs",
    fcp_conv_thr     = 1.E-2,
    freeze_all_atoms = False
    )

rism = dict(
   nsolv             = len(additional_cards)-1,
   closure           = 'kh',
   tempv             = 300.0,
   ecutsolv          = 160.0,
   starting1d        = 'zero',
   rism1d_conv_thr   = 1.0e-8,
   rism1d_maxstep    = 15000,
   mdiis1d_size      = 20,
   mdiis1d_step      = 0.2,
   starting3d        = 'zero',
   rism3d_maxstep    = 15000,
   rism3d_conv_thr   = 1.0e-6,
   rism3d_conv_level = 0.8,
   mdiis3d_size      = 20,
   mdiis3d_step      = 0.1,
   laue_buffer_right = 4.0,
   laue_expand_right = 60,
    )

kpts=(2, 2, 1)
koffset=(1, 1, 0)

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
if control["trism"]:
    print("   RISM  yes")
    system.update(system_update)
    if control["lfcp"]:
        print("   FCP   yes")
        input_data = dict(
            control = control,
            system = system,
            electrons=electrons,
            ions=ions,
            fcp = fcp,
            rism = rism,
        )
    else:
        print("   FCP   no")
        input_data = dict(
            control = control,
            system = system,
            electrons=electrons,
            ions=ions,
            rism = rism,
        )
    rism_update={}
    for count,atom in enumerate(atomic_species,start=1):
        rism_update[ "solute_lj({})".format(count) ] = "none"
        rism_update[ "solute_epsilon({})".format(count) ]=lj_parameter_database[atom]["epsilon"]
        rism_update[ "solute_sigma({})".format(count) ]=lj_parameter_database[atom]["sigma"]
    rism.update(rism_update)

else:
    print("   RISM  no")
    input_data = dict(
            control = control,
            system = system,
            electrons=electrons,
            ions=ions,
        )
    additional_cards=False

if vibration_mode:
    control["calculation"] = "scf"
    electrons["conv_thr"] = 1.E-8

# set calculator
calc = Espresso(
                input_data=input_data,
                pseudopotentials=pseudopotentials,
                additional_cards=additional_cards,
                kpts=kpts,koffset=koffset
                )
atoms.calc=calc

# set constraints
if set_constraint:
    # indices_fixing=[atom.index for atom in atoms if atom.position[2]< 11.0 ]
    indices_fixing=[atom.index for atom in atoms if atom.position[2]< -0.1 ]
    # indices_fixing=[atom.index for atom in atoms if atom.symbol == "Cu" ]
    c=FixAtoms(indices=indices_fixing)
    atoms.set_constraint(c)
    print("set constraint on atom index  : " , indices_fixing )
    print("set constraint on atom symbol : " , np.array(atoms.get_chemical_symbols())[indices_fixing])

# --------------------------------------------creating

if run_mode :
    if relax_mode or scf_mode:
        if relax_mode:
            print("performing relax mode")
        elif scf_mode:
             print("performing scf mode")

        write("init_structure.vasp",atoms,format="vasp")
        atoms.get_potential_energy()

        opt_atoms=read("espresso.pwo",format="espresso-out",index=-1)
        write("final_structure.vasp",opt_atoms,format="vasp")


    if vibration_mode:

        print("performing vibration mode")

        indices=[atom.index for atom in atoms if atom.symbol in [ "C", "N", "O", "H"]]
        print("calculate vibration for atoms index  : ", indices)
        print("calculate vibration for atoms symbol : ", np.array(atoms.get_chemical_symbols())[indices])

        vib = Vibrations(atoms,indices=indices)
        vib.run()
        vib.summary()

        vib_energies = vib.get_energies()
        vib_energies_real=vib_energies[np.isreal(vib_energies)]
        thermo = HarmonicThermo(vib_energies=vib_energies_real,
                potentialenergy=0.0)
        entro = thermo.get_entropy(temperature=298.15, verbose=True)
        inter = thermo.get_internal_energy(temperature=298.15, verbose=True)


if geninput_mode:

    fileout=open(outfilename,"w")
    write_espresso_in( fileout,
                      atoms,
                      input_data,
                      pseudopotentials=pseudopotentials,
                      kpts=kpts,koffset=koffset,
                      crystal_coordinates=False,
                      additional_cards=additional_cards)
    fileout.close()
    print("generated input file to ",outfilename)

