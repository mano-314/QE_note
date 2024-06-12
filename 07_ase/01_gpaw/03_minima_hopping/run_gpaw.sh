#!/bin/bash
#PBS -N test
#PBS -o _stdout
#PBS -e _stderr
#PBS -q mem192v2
#PBS -l nodes=1:ppn=32
NPROCS=32

cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1
#--------------------------------------------------------------


# 1) initialize python on compute node
source ~/.bashrc
conda activate gpaw


gpaw -P $NPROCS python minima.py







