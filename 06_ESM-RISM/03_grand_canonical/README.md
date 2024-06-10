1. First we obtain the Fermi level of neutral slab (at potential of zero charge)
2. calculate the electronic structure at -0.3 V vs PZC using FCP
3. calculate the electronic structure at -0.3 V vs PZC using GCSCF

**If one wants to include RISM, please turn on `trism  = .false.` 
and change the boundary condition to `esm_bc  = 'bc1'`.**

-------------
# References 

## Constant bias potential (constant-mu) method
- total energy
- charge density
- force
- potential of a polarized or charged slab

## ESM :
M. Otani and O. Sugino, PRB 73, 115407 (2006).

## constant-mu schemes: 

1. The fictitious charge particle (FCP) method
N. Bonnet, T. Morishita, O. Sugino, and M. Otani,PRL 109, 266101 (2012)

2. The grand canonical scf (GCSCF) method
R. Sundararaman, W. A. Goddard-III, and T. A. Arias, J. Chem. Phys. 146, 114104 (2017)



