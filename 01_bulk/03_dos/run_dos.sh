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


# 1) perform scf calculation to obtain charge density
mpirun -hostfile $PBS_NODEFILE -n $NPROCS pw.x -in scf.in > scf.out

# 2) start from charge density from previous scf calculation and expand on particular k-mesh
mpirun -hostfile $PBS_NODEFILE -n $NPROCS pw.x -in nscf.in > nscf.out

# 3) extract eigenvalues and calculate DOS
mpirun -hostfile $PBS_NODEFILE -n $NPROCS dos.x -in dos.in > dos.out

# 3) project wavefunction to calculate projected DOS
mpirun -hostfile $PBS_NODEFILE -n 2 projwfc.x -in projwfc.in > projwfc.out





