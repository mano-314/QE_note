#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem192v2
#PBS -l nodes=1:ppn=32
NPROCS=32

cd $PBS_O_WORKDIR
module purge
module load intel23-intelmpi  
module load fftw-3.3.9
module load hdf5-1.12.0
export PATH=/home/software/espresso/qe-7.2-intel23-intelmpi/bin/:$PATH

#--------------------------------------------------------------------------------------

#------------------------------------------------------------- WITH negative electric field 

# 1.1) solving KS equation with negative constant electric field 
mpirun -n $NPROCS pw.x -in scf_efield_n.in > scf_efield_n.out

# 1.2) extracting charge density 
mpirun -n $NPROCS pp.x -in post_rho.in > post_rho.out
mv rho.cube rho_efield_n.cube

# 1.3) extracting electrostatic potential 
mpirun -n $NPROCS pp.x -in post_phi.in > post_phi.out
mv electrostatic.cube electrostatic_efield_n.cube

# 1.4) extracting the sawtooth potential (= constant electric field)
mpirun -n $NPROCS pp.x -in post_sawtooth.in > post_sawtooth.out
mv sawtooth.cube sawtooth_efield_n.cube


#------------------------------------------------------------- WITH positive electric field

# 2.1) solving KS equation with positive constant electric field
mpirun -n $NPROCS pw.x -in scf_efield_p.in > scf_efield_p.out

# 2.2) extracting charge density
mpirun -n $NPROCS pp.x -in post_rho.in > post_rho.out
mv rho.cube rho_efield_p.cube

# 2.3) extracting electrostatic potential
mpirun -n $NPROCS pp.x -in post_phi.in > post_phi.out
mv electrostatic.cube electrostatic_efield_p.cube

# 2.4) extracting the sawtooth potential (= constant electric field)
mpirun -n $NPROCS pp.x -in post_sawtooth.in > post_sawtooth.out
mv sawtooth.cube sawtooth_efield_p.cube








