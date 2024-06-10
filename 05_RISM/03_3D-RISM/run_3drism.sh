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


# 1) perform calculation in 3D periodic boundary without RISM
mpirun -n $NPROCS pw.x -in scf_pbc.in > scf_pbc.out
mv output/opt.esm1 opt_pbc.esm1

# 2) post-process for the previous calculation to get electrostatic potential
mpirun -n $NPROCS pp.x -in post_phi.in > post_phi.out

# 3) run 3D-RISM
mpirun -n $NPROCS pw.x -in scf_rism.in > scf_rism.out
mv output/opt.esm1 opt_rism.esm1

# 4) post-process for 3D-RISM
mpirun -n $NPROCS pprism.x -in post_rism.in > post_rism.out 





