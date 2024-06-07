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
#    Since Bader is grid-based method, therefore the denser grid should give a more reliable integration 
#    We can compare how sensitive the integrated charge is when number of grid charged
mpirun -n $NPROCS pw.x -in scf.in > scf.out 

# 2) post-process using pp.x to get charge density (valence from scf)
mpirun -n $NPROCS pp.x -in post_rho.in > post_rho.out

# 3) post-process using pp.x to get charge density (core + valence)
mpirun -n $NPROCS pp.x -in post_ae.in > post_ae.out

# 5) calculate bader charge using bader code
#../script/bader distribution_rho.cube -ref distribution_ae.cube -p all_atom

# 5) use projwfc.x to project wavefunction onto s,p,d orbitals
#    By projecting, we can get Lowdin charge 
# mpirun -n 4 projwfc.x -in projwfc.in > projwfc.out





