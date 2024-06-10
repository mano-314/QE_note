#!/bin/bash

# This code is used to collect the solvation energy from
# the previously generated calculations
# and print out for further analysis
# $ bash energy.sh

for H2O_file in \
H2O.spc.Nishihara.MOL \
H2O.spce.Nishihara.MOL \
H2O.spce.Chuev.MOL \
H2O.spce.Matsugami.MOL \
H2O.tip5p.Nishihara.MOL \
; do

_gauss=$( grep GaussFluct ${H2O_file}/scf.out | awk '{print $2}' )
list_gauss=(${_gauss// / })
list_molec=($( grep Molecule ${H2O_file}/scf.out | awk '{print $5}' ))

N_gauss=${#list_gauss[@]}
N_molec=${#list_molec[@]}

index=0
pattern_1=H3O+
pattern_2=Total
for i in ${list_molec[@]}; do
 	for j in ${list_molec[@]} Total ; do 
		if [ $i == $pattern_1 ] ; then 
			if [ $j == $pattern_2 ] ; then
				echo $H2O_file $i $j $index   ${list_gauss[index]}
			fi 
		fi 
		index=$( echo " $index + 1 " | bc -l)
	done 
done
done 
