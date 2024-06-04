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

# 1) solving KS equation with periodic boudnary condition (xyz)
#mpirun -n $NPROCS pw.x -in scf_pbc.in > scf_pbc.out
#mv output/opt.esm1 profile_pbc.esm1

# 2) solving KS equation with mixed boundary condition / open in z-direction 
#    vacuum/slab/vacuum 
#mpirun -n $NPROCS pw.x -in scf_bc1.in > scf_bc1.out
#mv output/opt.esm1 profile_bc1.esm1

# 3) solving KS equation with mixed boundary condition / open in z-direction
#    vacuum/slab/metal
mpirun -n $NPROCS pw.x -in scf_bc2.in > scf_bc2.out
mv output/opt.esm1 profile_bc2.esm1

# 4) solving KS equation with mixed boundary condition / open in z-direction
#    metal/slab/metal
mpirun -n $NPROCS pw.x -in scf_bc3.in > scf_bc3.out
mv output/opt.esm1 profile_bc3.esm1









