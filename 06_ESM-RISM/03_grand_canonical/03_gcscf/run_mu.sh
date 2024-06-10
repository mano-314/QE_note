#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem192v2
#PBS -l nodes=1:ppn=32
NPROCS=32

cd $PBS_O_WORKDIR
module purge
#module load intel23-intelmpi
#module load fftw-3.3.9
#module load hdf5-1.12.0
#export PATH=/home/software/espresso/qe-7.2-intel23-intelmpi/bin/:$PATH


module load g16-a03
export PATH=/beegfs/coldpool/mano/qe/q-e/bin/:$PATH

#--------------------------------------------------------------------------------------


# 1) run GCSCF
mpirun -n $NPROCS pw.x -in scf.in > scf.out


