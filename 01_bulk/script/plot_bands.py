import numpy as np
import matplotlib.pyplot as plt 
import sys 
import re

"""
python plot_bands.py prefix 
"""

#-------------------------------------------- read fermi 

scffile="scf.out"
save_fermi=[]
with open(scffile) as f :
    scftext=f.read()
for match in re.finditer("Fermi",scftext):
    try:
        phrase=scftext[match.start():match.start()+30]
        _fermi=float(phrase.split()[3])
        save_fermi.append(_fermi)
    except:
        pass
fermi=save_fermi[-1]
print( "Fermi level  :", fermi )


#-------------------------------------------- read number information

prefix=sys.argv[1]
with open(prefix,"r") as f:
    line=f.readline()
    line=line.strip().split()
    nbnd=int(line[2].replace(",",""))
    nks=int(line[4])
print("read ... ", prefix )
print("number of bands   : ", nbnd)
print("number of kpoints : ", nks)


#-------------------------------------------- read eigenvalues

rawdata="{}.gnu".format(prefix); print("read ... ", rawdata )
data=np.loadtxt(rawdata); print("shape read from {} : ".format(rawdata) , data.shape)
data=data.reshape(nbnd,nks,-1); print("reshape to : " , data.shape)


#-------------------------------------------- plot band structures

plt.figure(figsize=(6,4))
for ibnd in range(nbnd) : 
    plt.plot(data[ibnd,:,0],data[ibnd,:,1]-fermi,c='black',lw=1.0)
plt.plot(plt.xlim(),[0,0],lw=0.5,c="black")
xmin,xmax=data[ibnd,:,0].min(), data[ibnd,:,0].max()
plt.xlabel("k path", fontsize=14); plt.ylabel("E - E$_f$ [eV]", fontsize=14)
plt.xlim(xmin,xmax); plt.ylim(-10,15)
plt.tight_layout()
plt.show()




