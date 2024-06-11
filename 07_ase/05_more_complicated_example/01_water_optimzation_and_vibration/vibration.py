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

run_mode       = True
relax_mode     = False
scf_mode       = False
vibration_mode = True
geninput_mode  = False
set_constraint = False

trism          = True
lfcp           = False
charge         = 0.0

pseudopotentials_dir = "/beegfs/hotpool/mano/rism/RISM_example/pseudo"
pseudopotentials = {
    "H" : "h_pbe_v1.4.uspp.F.UPF",
    "O" : 'o_pbe_v1.2.uspp.F.UPF' }

additional_cards = ["SOLVENTS {mol/L}",
                    "H2O -1.0 H2O.tip5p.Nishihara.MOL",
                    "K+   1.0 K+.Hagiwara.MOL",
                    "OH-  1.0 OH-.oplsaa.MOL" ]

lj_parameter_database={
    "H" :{"epsilon":0.046,  "sigma":1.00},
    "O" :{"epsilon":0.1554, "sigma":3.166} }

profile = EspressoProfile(
    command='mpirun -n 32 pw.x', pseudo_dir=pseudopotentials_dir
)

# -------------------------------------------------- DFT input

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
    ecutwfc     = 40,
    ecutrho     = 320.0,
    occupations = "smearing",
    smearing    = "gauss",
    degauss     = 0.01,
    nspin       = 1,
    nosym       = True,
    )

system_update=dict(
    assume_isolated = "esm",
    esm_bc = "bc1",
    tot_charge = charge,
)

electrons=dict(
    electron_maxstep=200,
    conv_thr=1.E-8,
    mixing_beta=0.1,
    # diagonalization='rmm',
    # startingwfc='file',
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
   laue_expand_left = 60,
   laue_expand_right = 60
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
    #rism["starting1d"] = 'file'
    #rism["starting3d"] = 'file'

# set calculator
calc = Espresso(profile=profile,
                input_data=input_data,
                pseudopotentials=pseudopotentials,
                additional_cards=additional_cards,
#                kpts=kpts,koffset=koffset
                )
atoms.calc=calc

# set constraints
if set_constraint:
    indices_fixing=[atom.index for atom in atoms if atom.position[2]< 0.0 ]
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

        #write("POSCAR_init",atoms,format="vasp")
        atoms.get_potential_energy()

        opt_atoms=read("espresso.pwo",format="espresso-out",index=-1)
        write("opt.vasp",opt_atoms,format="vasp")


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
        
        """
        thermo = HarmonicThermo(vib_energies=vib_energies_real,
                potentialenergy=0.0)
        entro = thermo.get_entropy(temperature=298.15, verbose=True)
        inter = thermo.get_internal_energy(temperature=298.15, verbose=True)
        """

        thermo = IdealGasThermo(vib_energies=vib_energies,
                        potentialenergy=0,
                        atoms=atoms,
                        geometry='nonlinear', spin=0, 
                        symmetrynumber=2 )
        G = thermo.get_gibbs_energy(temperature=298.15, pressure=101325.)


if geninput_mode:

    fileout=open(outfilename,"w")
    write_espresso_in( fileout,
                      atoms,
                      input_data,
                      pseudopotentials=pseudopotentials,
#                      kpts=kpts,koffset=koffset,
                      crystal_coordinates=False,
                      additional_cards=additional_cards)
    fileout.close()
    print("generated input file to ",outfilename)

