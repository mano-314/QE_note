import numpy as np 
import matplotlib.pyplot as plt 
import sys 

"""
python plot_esm.py esm_1 esm_2 ... index 
"""

fileins=sys.argv[1:-1]
index = int(sys.argv[-1])

for filein in fileins :

    print("reading ", filein)
    
    data = np.loadtxt(filein)
    yleft = data[0,index]
    ymin = data[:,index].min()
    plt.plot(data[:,0],data[:,index]-ymin,label=filein)
    
    xmin,xmax = data[:,0].min() , data[:,0].max()

plt.xlim(xmin,xmax)
plt.legend()
plt.show()


