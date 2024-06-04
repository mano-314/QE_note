Workflow for vibration (phonon) calculatin using phonopy 



1. Make displacement from optimized structure 
The symmetry operations are considered, therefore the number of displacements is reduced
Therefore, in principle, using phonopy should be faster than ASE in terms of less number 
of static scf required. If the anharmonicity is large, please check ALAMODE package. 

$ phonopy --qe -d --dim="1 1 1" -c init.in



2. Use script to run static scf calculations on every displacements 


$ ./gen_scf_calculations.sh



3. Collect forces from output files 

$ phonopy -f scf/supercell-*/super*out



4. make "mesh.conf" as an input for next step 

ATOM_NAME = O H
DIM = 1 1 1
MP = 1 1 1
EIGENVECTORS  = .TRUE.


5. execute phonopy to make the dynamical matrix and diagonalize it

$ phonopy -p mesh.conf
