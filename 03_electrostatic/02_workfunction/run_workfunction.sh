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

# 1.1) perform scf calculation
mpirun -n $NPROCS pw.x -in scf.in > scf.out

# 1.2) calculate electrostatic potential from the previous calculation
mpirun -n $NPROCS pp.x -in post_phi.in > post_phi.out

# 1.3) average the electrostatic potential in xy plane 
# average.x -in average.in 





