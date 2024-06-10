#!/bin/bash 

# This script is used to generate the set of calculations
# of 1D-RISM using various types of parametrization 
# to compare the solvation energy to the experiments 
# $ bash gen.sh

H3O_file=H3O+.chuev.MOL
Cl_file=Cl-.oplsaa.MOL
concentration=0.01

for H2O_file in \
H2O.spc.Nishihara.MOL \
H2O.spce.Nishihara.MOL \
H2O.spce.Chuev.MOL \
H2O.spce.Matsugami.MOL \
H2O.tip5p.Nishihara.MOL \
; do

if [ ! -d $H2O_file ] ; then mkdir $H2O_file ; fi 
cd $H2O_file
echo "enteres $H2O_file"

cat > scf.in <<!
&CONTROL
 calculation  = 'relax'
 outdir       = 'output'
 pseudo_dir   = '/beegfs/hotpool/mano/rism/RISM_example/pseudo/'
 prefix       = 'opt'
 trism        = .true.
/
&SYSTEM
 ibrav = 0,
 ntyp = 1,
 nat = 1
 nbnd = 2
 ecutwfc = 40,
 ecutrho = 320
 occupations = "smearing",
 smearing = "gauss",
 degauss = 0.01
 tot_charge = 0.0
/
&ELECTRONS
 electron_maxstep = 200,
 mixing_beta = 0.1,
/
&IONS
 ion_dynamics = 'bfgs'
 upscale = 1.d0
/
&RISM
 nsolv = 3,
 closure  = 'kh'
 tempv = 300,
 ecutsolv = 160
 solute_lj(1) = 'none', solute_epsilon(1) = 0.1554, solute_sigma(1) = 3.166 !TIP5P O
 solute_lj(2) = 'none', solute_epsilon(2) = 0.0460, solute_sigma(2) = 1.000 !modified H
 starting1d       = 'zero'
 rism1d_conv_thr  = 1e-08
 rism1d_maxstep   = 15000
 mdiis1d_size     = 10
 mdiis1d_step     = 0.1
/

K_POINTS gamma

SOLVENTS {mol/L}
H2O   -1.0    ${H2O_file}
H3O+   ${concentration}  ${H3O_file}
Cl-    ${concentration}  ${Cl_file}

ATOMIC_SPECIES
H   1.008  h_pbe_v1.4.uspp.F.UPF

CELL_PARAMETERS angstrom
20.0 0.0 0.0
0.0 20.0 0.0
0.0 0.0 20.0

ATOMIC_POSITIONS (angstrom)
H 0.0 0.0 0.0

!

cp ../run_1drism.sh .
qsub run_1drism.sh

cd ../

done 




