E_SHE                   = 5.243
E_RHE                   = 4.414
E_Fermi_at_charge_zero  = 4.5919

E_pzc  = E_Fermi_at_charge_zero - E_SHE

print("E_SHE    : {:4.3f} V".format(E_SHE))
print("E_RHE    : {:4.3f} V (pH=14)".format(E_RHE))
print("E_Fermi  : {:4.3f} V".format(E_Fermi_at_charge_zero) )
print("E_pzc    : {:4.3f} V".format(E_pzc))


import numpy as np 
import matplotlib.pyplot as plt 

data=np.loadtxt("dos.dos")
x=data[:,0]
y=data[:,1]
plt.figure(figsize=(6,2))
plt.plot(x,y,lw=2.0,c="black")
ymin,ymax=plt.ylim()
xmin,xmax=-10,0
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.plot([-E_Fermi_at_charge_zero,-E_Fermi_at_charge_zero],[ymin,ymax],lw=2.0,c="red",label="E_Fermi")
plt.plot([-E_SHE,-E_SHE],[ymin,ymax],lw=2.0,c="blue",label="E_SHE")
plt.plot([-E_RHE,-E_RHE],[ymin,ymax],lw=2.0,c="green",label="E_RHE")
plt.xlabel("E vs $\Phi_S$",fontsize=12)
plt.ylabel("DOS",fontsize=12)
plt.legend(frameon=False)
plt.tight_layout()
plt.show()


