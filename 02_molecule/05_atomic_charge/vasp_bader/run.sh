#!/bin/bash
#PBS -N vasp
#PBS -o out
#PBS -e err
#PBS -q mem96
#PBS -l nodes=1:ppn=16

VASPEXE=/home/software/vasp/vasp-6.4.1/intel19/vasp.6.4.1-std-intel19-openmpi-4.1.1

module purge
module load gnu-7.5.0
module load intel19-openmpi-4.1.1
module load hdf5-1.12.0

cd $PBS_O_WORKDIR
echo '======================================================='
echo Working directory is $PBS_O_WORKDIR
echo "Starting on `hostname` at `date` "
if [ -n "$PBS_NODEFILE" ]; then
   if [ -f $PBS_NODEFILE ]; then
      echo "Nodes used for this job:"
      cat ${PBS_NODEFILE}
      NPROCS=`wc -l < $PBS_NODEFILE`
   fi
fi
mpirun -hostfile $PBS_NODEFILE -n $NPROCS $VASPEXE > log
echo "Job Ended at `date` "
echo '======================================================='
