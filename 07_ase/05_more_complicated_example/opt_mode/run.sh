#!/bin/bash -l
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=128
#SBATCH -t 24:00:00
#SBATCH -J opt
#SBATCH -A lt200241

module purge
module load intel/2023.1.0
module load libfabric/1.15.2.0
module load Mamba/23.11.0-0

source ~/.bashrc 
conda init
conda activate atomic 

export OMP_NUM_THREADS=1
ulimit -s unlimited
cd $SLURM_SUBMIT_DIR

export PATH=/home/pmano/software/qe-7.3_environ/bin/:$PATH
#export PATH=/home/pmano/software/qe-dev/bin/:$PATH
export ASE_ESPRESSO_COMMAND="srun pw.x -nk 2 -in espresso.pwi > espresso.pwo"

python opt.py init.vasp
