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

mpirun -n $NPROCS pw.x -in iso_CO.in > iso_CO.out
mpirun -n $NPROCS pw.x -in clean.in > clean.out
mpirun -n $NPROCS pw.x -in top.in > top.out
mpirun -n $NPROCS pw.x -in hollow.in > hollow.out
mpirun -n $NPROCS pw.x -in bridge.in > bridge.out




