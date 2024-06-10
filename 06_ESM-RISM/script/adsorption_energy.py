import re
import sys
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



U_SHE                    = -5.243
switch_on_points_label   = True
ry2ev                    = 13.605662285137
ne_slab                  = 228
path_to_files            = "./results/charge*"

#-------------------------------------------------- create functions 

def read_out(filename):
    with open(filename) as f :
        lines=f.read()

    save_fermi = []
    for match in re.finditer("Fermi energy is",lines):
        startindex=match.start()
        block=lines[startindex:startindex+29].split()
        save_fermi.append(float(block[3]))

    save_free_energy = []
    for match in re.finditer("! ",lines):
        startindex=match.start()
        block=lines[startindex:startindex+60].split()
        save_free_energy.append(float(block[4])*ry2ev)

    save_electrons = []
    for match in re.finditer("number of electrons",lines):
        startindex=match.start()
        block=lines[startindex:startindex+60].split()
        save_electrons.append(float(block[4]))

    return save_free_energy[-1] , save_fermi[-1] , save_electrons[0]

def cal_charge(x, Q_0, C_dl_0, Delta_0, A):
    charge = Q_0 + A*C_dl_0*x + A*Delta_0*0.5*x**2
    return charge

def fitfunction(tofit_x,tofit_y):
    fit=np.polyfit(tofit_x,tofit_y,3)
    func=np.poly1d(fit)
    print("\n--------------------------------------- function ---------------------------------------")
    print(func)
    print("------------------------------------------------------------------------------------------\n")
    return func

def get_data_from_path(path_to_files):
    files=glob.glob(path_to_files)
    files.sort()
    save_all=[]
    for file in files:
        try :
            free_energy,fermi,nelect = read_out(file)
            save_block=[free_energy,fermi,nelect,file]
            save_all.append(save_block)
        except:
            pass
    print("read data from                       : ", path_to_files)
    return save_all

def make_dataframe(data_list,ne_ads,U_SHE,write_csv=False,csv_file="ads.csv"):
    df=pd.DataFrame(data=data_list,columns=["free energy","fermi","nelect","filename"])
    df.sort_values(by="fermi",inplace=True)
    df["grand_potential"]=df["free energy"] - (df["nelect"] - ne_ads) * df["fermi"]
    df["pot_she"]=(df["fermi"] - U_SHE)*-1.0
    df["charge"] = ne_ads - df["nelect"]
    if write_csv:
        df.to_csv(csv_file,index=None)
        print("write table to                       : ", csv_file)
    print("\n--------------------------------------- TABLE ---------------------------------------")
    print(df)
    print("---------------------------------------------------------------------------------------\n")
    return df

#--------------------------------------------------

print("starting electrode potential (U_SHE) : {:6.4f}".format(U_SHE))
print("starting number of electrons (bare)  : {:6d}".format(ne_slab))

fig=plt.figure(figsize=(5,4))

#-------------------------------------------------- read data from files 
save_all=get_data_from_path(path_to_files)
slab=make_dataframe(save_all,ne_slab,U_SHE,write_csv=False,csv_file="bare.csv")

#-------------------------------------------------- fitting data to equation 
x_slab=slab["pot_she"].values
y_slab=slab["grand_potential"].values 
xmin,xmax=x_slab.min(),x_slab.max()
func_slab=fitfunction(x_slab,y_slab)
xt_slab=np.linspace(xmin,xmax,1000)
yt_slab=func_slab(xt_slab)

#-------------------------------------------------- plotting 
grand_shift=yt_slab.max()
plt.plot(xt_slab,yt_slab-grand_shift,c='firebrick',lw=2.0)
plt.scatter(x_slab,y_slab-grand_shift,marker="o",s=30,edgecolor="firebrick",label="cu slab",facecolor="none")

bare_pzc = xt_slab[np.argmax(yt_slab)]
print( "the grand potential [ {:6.3f} eV ] is shifted to [ 0 eV ]".format(grand_shift))

if switch_on_points_label:
    for count, _file in enumerate(slab["filename"].values):
        plt.text( x_slab[count],y_slab[count]-grand_shift , _file, fontsize = 9)
print(bare_pzc)
ymin,ymax=plt.ylim()
plt.ylim(ymin,ymax)
plt.yticks(fontsize=14);plt.xticks(fontsize=14)
plt.ylabel("$\Omega$ [eV]",fontsize=16)
plt.xlabel("U vs. SHE [V]",fontsize=16)
plt.legend(frameon=False,markerfirst=False,fontsize=13,#loc="upper right",
           handletextpad=0.00,labelspacing=0.1) #,bbox_to_anchor=(1.08,1.03))

# plt.savefig("grand_potential.png",dpi=400,bbox_inches="tight",transparent=True)
plt.tight_layout()
plt.show()



