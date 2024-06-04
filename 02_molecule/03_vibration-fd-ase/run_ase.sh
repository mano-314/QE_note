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


# 1) initialize python on compute node
source ~/.bashrc
conda activate rism

# 2) execute the python script file for vibration using ase module 
#    Note that the command is specified inside the python script since ASE version 3.23
#    for version older than 3.22, we have to specify the environment variable ASE_ESPRESSO_COMMAND
#    $ export ASE_ESPRESSO_COMMAND="mpirun -n XX pw.x -in espresso.pwi > espresso.pwo"
python vibration_ase.py init.in



