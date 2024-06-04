# QE_note

The electrode-electrolyte interface simulation using Quantum Espresso

---------------------------------------------
Requirements
QE
- pw.x / ph.x / pp.x / bands.x / dos.x / rism.x / pprism.x / rism1d.x

python
- numpy / matplotlib / phonopy / ase

---------------------------------------------

SET UP AN ENVIRONMENT

to use qe, we need to load intel module
```
  $ module load intel22-openmpi-4.1.2
```
and don't forget to put this in jobscript file too

to use python, we need to load anaconda module
```
  $ module load anaconda3.8
  $ source ~/.bashrc
```

and it will be better to create your own environment,
for example, to make the environment with python3.9 named rism,
```
  $ conda create -n rism python=3.9
  $ conda activate rism
```

and we need ase and phonopy, which can be easily installed by
```
  $ pip install ase
  $ pip install phonopy
```

and to activate this in compute node, put the following command into jobscript file
```
  $ source ~/.bashrc
  $ conda activate rism
```

   < NOTE >
   ASE is already install in this cluster, but we need to modify the code to make it
   available for using integrated with rism. That's why we need our own environment >

---------------------------------------------

1. **BULK**

QE was developed based on plane wave representation for solving KS-equation.
It was fitted for the calculation in solid states, which is the original spirit of QE.
Therefore, it is good the start from looking at the solid properties, especially the
representative ones; band structures and density of states

1) optimization
2) bandstructure
3) dos

#---------------------------------------------

2. **MOLECULE**

In our study of electrochemical system, the calculation involving gthe isolated molecule is required,
Furthermore, the calculation of vibrational frequencies is very important in determining the ZPE, entropy and so on.
In this section, we will look at how to simulate the isolated molecule as well as the vibrational frequencies using
two different approaches; density functional purterbation theory (DFPT) and the finite displacement methid (FDM)
to calculate phonon. For FDM, which is not directly implemented in QE, the external tools (phonopy and ase) are introduces here.
At the end of this section, the electron density and the electrostatic potential obtained from the calculation are exported.
By making the planar average, the density profile in particular direction can be obtained and we will realize that
how dipole of water affect of electrostatic potential.

1) optimization
2) vibration-dfpt
3) vibration-fd-ase
4) vibration-fd-phonopy
5) rho_and_phi

#---------------------------------------------

3. **ELECTROSTATIC**

We have seen from the previous section that the electrostatic potential of the non-zero dipole system is difficult to defined
in a presence of periodic boundary condition. Here, we are provided with two methods to treate the dipole;
(I) the dipole correction in a recipe of [L. Bengtsson, PRB 59, 12301 (1999)]
and (II) the open boundary recipe of [M. Otani and O. Sugino, PRB 73, 115407 (2006)]
The examples using water molecule are presented in 1) and 2), while the slab models are shown in 3), 4) and 5).
the example 3) follows (I) method which can be extended into the imposing of the constant electric field as a sawtooth potential in 4).
For the different ways to consider the electric field, the example 5) using method (II) is provided here.


1) H2O_dipole_correction
2) H2O_OBC
3) slab_dipole_correction
4) slab_efield_constant
5) slab_efield_ESM


