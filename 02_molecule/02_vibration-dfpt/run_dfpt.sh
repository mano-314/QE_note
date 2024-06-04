#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem192v2
#PBS -l nodes=1:ppn=16
NPROCS=16

cd $PBS_O_WORKDIR
module purge
module load intel23-intelmpi  
module load fftw-3.3.9
module load hdf5-1.12.0
export PATH=/home/software/espresso/qe-7.2-intel23-intelmpi/bin/:$PATH

#--------------------------------------------------------------


# 1) perform scf calculation
mpirun -n $NPROCS pw.x -in scf.in > scf.out 

# 2) perform DFPT calculation to obtain the dynamical matrix
mpirun -n $NPROCS ph.x -in ph.in > ph.out

# 3) reads a dynamical matrix, diagonalises, and applies the Acoustic Sum Rule
dynmat.x -in dyn.in > dyn.out 



