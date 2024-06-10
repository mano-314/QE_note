import numpy as np 
import re 
import sys 
filein=sys.argv[1]

pattern_charge="!    total charge of GC-SCF    ="
pattern_energy="!    total energy"
pattern_fermi = "the Fermi energy is"

with open(filein) as f :
    text=f.read()

save_charge=[]
for match in re.finditer(pattern_charge,text):
    phrase=text[match.start():match.start()+60].split()[6]
    save_charge.append(float(phrase))

save_energy=[]
for match in re.finditer(pattern_energy,text):
    phrase=text[match.start():match.start()+60].split()[4]
    save_energy.append(float(phrase))

save_fermi=[]
for match in re.finditer(pattern_fermi,text):
    phrase=text[match.start():match.start()+60].split()[4]
    save_fermi.append(float(phrase))

#print("Charge : " , save_charge)
#print("Energy : " , save_energy)
#print("Fermi  : " , save_fermi)

print("iter       energy      fermi    charge")
for count in range(len(save_energy)):
    print("{:3d}  {:8.6f}  {:8.6f}  {:8.6f}".format(count , save_energy[count], save_fermi[count] , save_charge[count]) )


