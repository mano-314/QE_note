#!/bin/bash
#PBS -N qe
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem192v2
#PBS -l nodes=1:ppn=32
NPROCS=32

cd $PBS_O_WORKDIR
module purge
module load g16-a03
export PATH=/beegfs/coldpool/mano/qe/q-e/bin/:$PATH

#--------------------------------------------------------------


# 1) initialize python on compute node
source ~/.bashrc
conda activate rism

# 2) execute the python script file for vibration using ase module 
#    Note that the command is specified inside the python script since ASE version 3.23
#    for version older than 3.22, we have to specify the environment variable ASE_ESPRESSO_COMMAND
#    $ export ASE_ESPRESSO_COMMAND="mpirun -n XX pw.x -in espresso.pwi > espresso.pwo"
#    for old version, RISM input is not supported
#    after version 3.23, RISM input is supported

python optimization.py cu111.vasp




