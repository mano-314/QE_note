#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem96
#PBS -l nodes=1:ppn=32
NPROCS=32

cd $PBS_O_WORKDIR
module purge
module load intel23-intelmpi  
module load fftw-3.3.9
module load hdf5-1.12.0
export PATH=/home/software/espresso/qe-7.2-intel23-intelmpi/bin/:$PATH

#--------------------------------------------------------------------------------------

#------------------------------------------------------------- WITHOUT dipole correction
# 1.1) perform scf calculation (WITHOUT dipole correction)
mpirun -n $NPROCS pw.x -in scf_none.in > scf_none.out

# 1.2) calculate electrostatic potential from the previous calculation
mpirun -n $NPROCS pp.x -in post.in > post.out
mv electrostatic.cube electrostatic_none.cube



#------------------------------------------------------------- WITH dipole correction
# 2.1) perform scf calculation (WITH dipole correction)
mpirun -n $NPROCS pw.x -in scf_dipole.in > scf_dipole.out

# 2.2) calculate electrostatic potential from the previous calculation 
mpirun -n $NPROCS pp.x -in post.in > post.out
mv electrostatic.cube electrostatic_dipole.cube

# 2.3) extract sawtooth potential applied in the potential correction 
mpirun -n $NPROCS pp.x -in post_sawtooth.in > post_sawtooth.out
mv sawtooth.cube sawtooth_dipole.cube






