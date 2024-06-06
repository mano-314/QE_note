#!/bin/bash 

rytoev=13.6057039763

clean_energy=0
co_energy=0
top_energy=0
bridge_energy=0
hollow_energy=0

dirs=`ls -d */`

printf "%10s  %6s  %6s  %6s \n" XC T B H

#for dir in $dirs ; do 
for dir in pbe pbe+d3 vdw-df2 rpbe beef ; do 

printf "%10s " $dir 

if [ -f ${dir}/clean.out ] ; then 
clean_energy=$( grep ! ${dir}/clean.out | tail -n1 | awk '{print $5}')
fi 

if [ -f ${dir}/iso_CO.out ] ; then
co_energy=$(grep ! ${dir}/iso_CO.out | tail -n1 | awk '{print $5}')
fi

if [ -f ${dir}/top.out ] ; then
top_energy=$(grep ! ${dir}/top.out | tail -n1 | awk '{print $5}')
top_ads=$( echo " ( $top_energy - $co_energy - $clean_energy ) * $rytoev " | bc -l )
else top_ads=0 ; fi 

if [ -f ${dir}/bridge.out ] ; then
bridge_energy=$(grep ! ${dir}/bridge.out | tail -n1 | awk '{print $5}')
bridge_ads=$( echo " ( $bridge_energy - $co_energy - $clean_energy ) * $rytoev " | bc -l )
else bridge_ads=0 ; fi

if [ -f ${dir}/hollow.out ] ; then
hollow_energy=$(grep ! ${dir}/hollow.out | tail -n1 | awk '{print $5}')
hollow_ads=$( echo " ( $hollow_energy - $co_energy - $clean_energy ) * $rytoev " | bc -l )
else hollow_ads=0 ; fi

printf " %6.3f  %6.3f  %6.3f \n" $top_ads $bridge_ads $hollow_ads
#printf " top       :   %6.3f   eV\n" $top_ads
#printf " bridge    :   %6.3f   eV\n" $bridge_ads
#printf " hollow    :   %6.3f   eV\n" $hollow_ads

done 



