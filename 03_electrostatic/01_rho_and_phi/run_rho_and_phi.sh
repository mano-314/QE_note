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
mpirun -n $NPROCS pw.x -in scf.in > scf.out 

# 2) post-process using pp.x to get charge density (valence from scf) in cube file format 
mpirun -n $NPROCS pp.x -in post_rho.in > post_rho.out

# 3) post-process using pp.x to get electrostatic potential in cube file format
mpirun -n $NPROCS pp.x -in post_phi.in > post_phi.out

# 4) use some tools to visualize, integrate and so on 
