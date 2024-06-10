#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem96
#PBS -l nodes=1:ppn=16
NPROCS=16

cd $PBS_O_WORKDIR
module purge
#module load intel23-intelmpi  
#module load fftw-3.3.9
#module load hdf5-1.12.0
#export PATH=/home/software/espresso/qe-7.2-intel23-intelmpi/bin/:$PATH


module load g16-a03
export PATH=/beegfs/coldpool/mano/qe/q-e/bin/:$PATH

#--------------------------------------------------------------------------------------

# 1) calculate 1D-RISM using rism1d.x
#    this will solve 1D-RISM equation to describe solvent-solvent interaction 
#    therefore, the explicit part will be not included in the calculation
mpirun -n $NPROCS rism1d.x -in scf.in > scf.out





