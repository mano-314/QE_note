import numpy as np 
import matplotlib.pyplot as plt 
import sys 

"""
python plot_dos.py dos.dos
"""

filein=sys.argv[1]

#-------------------------------------------- read file 
with open(filein) as f:
    line=f.readline()
    fermi=float(line.split()[-2])
    print("fermi energy is ",fermi)

data=np.loadtxt(filein)
energy=data[:,0]-fermi 
dosup=data[:,1]
dosdn=data[:,2]

#-------------------------------------------- plot dos 
plt.plot(energy,dosup,c="black")
plt.plot(energy,-dosdn,c="black")

ymax=np.max([dosup.max(),dosdn.max()])
plt.plot([0,0],[-ymax,ymax],lw=0.5,c="black")
plt.plot([energy.min(),energy.max()],[0,0],lw=0.5,c="black")

plt.ylabel("DOS",fontsize=12)
plt.xlabel("E-E$_f$",fontsize=12)
plt.xlim(-10,10)
#plt.ylim(-ymax,ymax)
plt.ylim(-5,5)
plt.show()
