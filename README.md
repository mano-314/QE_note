# The electrode-electrolyte interface simulation using Quantum Espresso

**Requirements QE**
- pw.x / ph.x / pp.x / bands.x / dos.x / rism.x / pprism.x / rism1d.x

**Requirements python**
- numpy / matplotlib / phonopy / ase

---------------------------------------------

## SET UP AN ENVIRONMENT

to use qe, we need to load intel module
```
module load intel22-openmpi-4.1.2
```
and don't forget to put this in jobscript file too

to use python, we need to load anaconda module
```
module load anaconda3.8
source ~/.bashrc
```

and it will be better to create your own environment,
for example, to make the environment with python3.9 named rism,
```
conda create -n rism python=3.9
conda activate rism
```

and we need ase and phonopy, which can be easily installed by
```
pip install ase
pip install phonopy
```

and to activate this in compute node, put the following command into jobscript file
```
source ~/.bashrc
conda activate rism
```

_<NOTE>_
_ASE is already install in this cluster, but we need to modify the code to make it available for using integrated with rism. That's why we need our own environment_


## CONTENT 
### 1. **BULK**

QE was developed based on plane wave representation for solving KS-equation.
It was fitted for the calculation in solid states, which is the original spirit of QE.
We will start from looking at the representative properties; band structures and density of states

1) optimization
2) bandstructure
3) dos


### 2. **MOLECULE**

In the study of electrochemical system, the calculations involving the isolated molecule (or isolated system/ 2D) are required. 
Moreover, the calculation of vibrational properties is very important in determining the ZPE, entropy and so on.
In this section, we will look at how to simulate the isolated molecule as well as the vibrational frequencies using
two different approaches; density functional purterbation theory (DFPT) and the finite displacement method (FDM). 
For FDM, which is not directly implemented in QE, the external tools (ASE and Phonopy) are introduced here.
Next, the calculation of the atomic charge in Bader scheme will be introduced. 
At the end of this section, the electron density and the electrostatic potential obtained from the calculation are extracted. 
By performing the planar average, the density profile in particular direction can be obtained. 

1) optimization
2) vibration (dfpt)
3) vibration (fd-ase)
4) vibration (fd-phonopy)
5) atomic charge (Bader and Lowdin)


### 3. **ELECTROSTATIC**

At the beginning of this section, the electron density and the electrostatic potential obtained from the calculation are extracted.
By performing the planar average, the density profile in particular direction can be obtained.
We will see that the electrostatic potential of the non-zero dipole system under periodic treatment is difficult to define and diverged.
Here, we are provided with two methods to treat the dipole;
(I) the dipole correction in a recipe of _[L. Bengtsson, PRB 59, 12301 (1999)]_
and (II) the open boundary recipe of _[M. Otani and O. Sugino, PRB 73, 115407 (2006)]_
The examples using water molecule are presented in 1) and 2), while the slab models are shown in 3), 4) and 5).
the example 3) follows (I) method which can be extended into the imposing of the constant electric field using sawtooth potential in 4).
For the different ways to consider the bias potential, the example 5) using method (II) is provided here.

1) charge density and electrostatic potential 
2) Dipole correction (H2O)
3) Mixed boundary condition (H2O)
4) Dipole correction (slab) 
5) Constant electric field (sawtooth potential)
6) Bias potential using ESM (Effective Screening Medium) 
- Isolated slab (vacuum/slab/vacuum)
- Charged slab (vacuum/slab/metal)
- Slab under an electric field (metal/slab/metal)



--------------------------

**will be updated later**

### 4. **IMPLICIT SOLVENT**
1) Linearized Poisson-Boltzmann model

### 5. **RISM (Reference interaction site model)**
1) 1D-RISM : pair distribution & coordination number
2) 1D-RISM : Force field setting and solvation energy 
3) 3D-RISM : For periodic system 
4) Laue RISM : periodic in xy-plane and opened in z-direction
5) The determination of SHE potential 

### 6. **ESM-RISM**
1) The determination of PZC (potential of zero charge)
2) Constant Ne (electrons) calculation 
3) Constant mu (potential) calculation 
4) Grand potential calculation 
5) Adsorption energy as a function of potential


### 7. **ASE (Atomic simulation environment)**
1) How to make/manipulate structure from ASE
2) How to optimize structure using ASE optimizer with QE as calculator 
3) How to control QE from ASE script 
4) How to calculate vibration 
5) How to use ASE with RISM 



