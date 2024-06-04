#!/bin/bash 



# 1) please change the path to your pseudopotential  --------------------------
path_to_pseudopotential=/beegfs/hotpool/mano/rism/RISM_example/pseudo



# 2) get files list
files=`ls -f supercell*in | sed "s/.in//g"`



# 3) make directory for all static scf calculations ---------------------------
if [ ! -d scf ] ; then mkdir scf ; fi 



# 4) loop over displacements --------------------------------------------------

cd scf

for file in $files ; do 

echo $file 
if [ ! -d ${file} ] ; then mkdir $file ; fi 
cd  $file 
echo " entered $file "

cat > ${file}.in <<!
&CONTROL
   calculation      = 'scf'
   outdir           = 'output'
   prefix           = 'opt'
   pseudo_dir       = '${path_to_pseudopotential}'
   disk_io          = "nowf"
   tprnfor          = .true.
/
&SYSTEM
   ibrav            = 0
   ecutwfc          = 40
   ecutrho          = 320.0
   nspin            = 1
   ntyp             = 2
   nat              = 3
/
&ELECTRONS
   conv_thr         = 1e-08
   mixing_beta      = 0.3
/
&IONS
/
&CELL
/

K_POINTS gamma

!

cat ../../${file}.in >> ${file}.in
cp ../../run_phonopy.sh .
sed -i "s/replace_here/${file}/g" run_phonopy.sh

qsub run_phonopy.sh

cd ../
done 

cd ../



# 5) Everthing is done --------------------------------------------------------
echo "DONE"




