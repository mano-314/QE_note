import numpy as np 
import matplotlib.pyplot as plt 
import sys 
import re

"""
python plot_pdos.py file_1 file_2 index
"""

argv=sys.argv[1:]
files=argv[:-1]
index_to_plot=int(argv[-1])
scffile="scf.out"

#-------------------------------------------- read fermi from scf.out 

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


#--------------------------------------------- read pdos and plot 
plt.figure(figsize=(6,3))
for _file in files:
    print("plotting from file ... " , _file )
    data=np.loadtxt(_file)
    x=data[:,0]-fermi ;y=data[:,index_to_plot]
    plt.plot(x,y,label=_file,lw=2.0)
xmin,xmax=x.min(),x.max()
#plt.xlim(xmin,xmax)
plt.ylabel("projected DOS",fontsize=12)
plt.xlabel("E-E$_f$",fontsize=12)
plt.xlim(-10,10)
plt.legend(frameon=False)
plt.show()
