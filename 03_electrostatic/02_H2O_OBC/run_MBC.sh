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

#--------------------------------------------------------------------------------------

#------------------------------------------------------------- WITH 3-dimensional periodic boundary condition
# 1.1) perform scf calculation 
mpirun -n $NPROCS pw.x -in scf_pbc.in > scf_pbc.out

# 1.2) post-process to get the electrostatic potential 
mpirun -n $NPROCS pp.x -in post.in > post.out

# 1.3) save necessary files and remove unnecessary file
mv electrostatic.cube electrostatic_pbc.cube
mv output/opt.esm1 opt_pbc.esm1
rm optcharge


#------------------------------------------------------------- WITH 2-dimensional PBC in xy and use open boundary in z-direction 
# 2.1) perform scf calculation
mpirun -n $NPROCS pw.x -in scf_bc1.in > scf_bc1.out

# 2.2) post-process to get the electrostatic potential
mpirun -n $NPROCS pp.x -in post.in > post.out

# 2.3) save necessary files and remove unnecessary file
mv electrostatic.cube electrostatic_bc1.cube
mv output/opt.esm1 opt_bc1.esm1
rm optcharge





