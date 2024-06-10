import re
import sys
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
ry2ev=13.605662285137

# ------------------------------------ input params V2

plot_labels     = ["surface", "config-1", "config-2", "config-3", "config-4"]
path_to_bare="charge*"
# ------------------------------------ def functions
U_SHE           = -5.243
switch_on_points_label=True

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
    print(func)
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
    print("  read data from  : ", path_to_files)
    return save_all

def make_dataframe(data_list,ne_ads,U_SHE,write_csv=False,csv_file="ads.csv"):
    df=pd.DataFrame(data=data_list,columns=["free energy","fermi","nelect","filename"])
    df.sort_values(by="fermi",inplace=True)
    df["grand_potential"]=df["free energy"] - (df["nelect"] - ne_ads) * df["fermi"]
    df["pot_she"]=(df["fermi"] - U_SHE)*-1.0
    df["charge"] = ne_ads - df["nelect"]
    if write_csv:
        df.to_csv(csv_file,index=None)
        print("  wrote table to  : ", csv_file)
    print(df)
    return df

# ------------------------------------ read data (bare and ads) and fitting

ne_slab=228 #parameters[surface]["bare"]["nelect-bare"]
#A_mol_zpe=parameters[surface]["bare"]["zpe-free"]
print("starting calulcation for mode :  bare surface")
print(" starting number of electrons (bare) : ", ne_slab)
#print(" zpe for molecule             (free) : ", A_mol_zpe)

fig=plt.figure(figsize=(4,4))
colors_list=["red","blue","green","orange"]

save_all=get_data_from_path(path_to_bare)
slab=make_dataframe(save_all,ne_slab,U_SHE,write_csv=True,csv_file="bare.csv")

x_slab=slab["pot_she"].values
y_slab=slab["grand_potential"].values #+ A_ads + A_mol_zpe

xmin,xmax=x_slab.min(),x_slab.max()

func_slab=fitfunction(x_slab,y_slab)
xt_slab=np.linspace(xmin,xmax,1000)
yt_slab=func_slab(xt_slab)

grand_shift=yt_slab.max()
grand_left_save = yt_slab.copy()

plt.plot(xt_slab,yt_slab-grand_shift,c='black',lw=2.0)
plt.scatter(x_slab,y_slab-grand_shift,marker="o",s=30,edgecolor="black",label=plot_labels[0],facecolor="none")

bare_pzc = xt_slab[np.argmax(yt_slab)]

print( "\nthe grand potential [ {:6.3f} eV ] is shifted to [ 0 eV ]".format(grand_shift))
"""
for counter, path_to_ads in enumerate(path_to_ads_list):

    print("\nstarting calulcation for mode : ", modes[counter])
    ne_ads    = parameters[surface][modes[counter]]["nelect-ads"]
    A_ads_zpe = parameters[surface][modes[counter]]["zpe-ads"]
    print(" starting number of electrons (ads)  : ", ne_ads)
    print(" zpe for molecule             (ads)  : ", A_ads_zpe)

    save_all=get_data_from_path(path_to_ads)
    slabads=make_dataframe(save_all,ne_ads,U_SHE,write_csv=True,csv_file="ads_{}.csv".format(modes[counter]))

    x_slabads=slabads.copy()["pot_she"].values
    y_slabads=slabads.copy()["grand_potential"].values + A_ads_zpe

    func_slabads=fitfunction(x_slabads,y_slabads)
    xtmin,xtmax=x_slabads.min(),x_slabads.max()
    xt_slabads=np.linspace(xtmin,xtmax,1000)
    yt_slabads=func_slabads(xt_slabads)

    grand_right_save = yt_slabads.copy()
    crossing_point=xt_slabads[np.argmin(np.abs(grand_right_save-grand_left_save))]
    print( "  crossing point  : {:8.4f} eV".format(crossing_point))

    # ------------------------------------ plotting
    plt.plot(xt_slabads,yt_slabads-grand_shift,c=colors_list[counter],lw=2.0)
    plt.scatter(x_slabads,y_slabads-grand_shift,edgecolor=colors_list[counter],marker="o",s=30,label=plot_labels[1+counter],facecolor="none")

    plt.plot(xt_slabads,yt_slabads-yt_slab,c=colors_list[counter],lw=1.0,label=plot_labels[1+counter],ls="dashed")

    if switch_on_points_label:
        #for count, _file in enumerate(slab["filename"].values):
        #    plt.text( x_slab[count],y_slab[count]-grand_shift , _file.replace(surface,"").replace("charge","") , fontsize = 9)

        for count, _file in enumerate(slabads["filename"].values):
            plt.text( x_slabads[count],y_slabads[count]-grand_shift , _file.replace(surface + "-NO3","").replace(modes[counter],"") , fontsize = 9)
"""
if switch_on_points_label:
    for count, _file in enumerate(slab["filename"].values):
        plt.text( x_slab[count],y_slab[count]-grand_shift , _file, fontsize = 9)

ymin,ymax=plt.ylim()
plt.ylim(ymin,ymax)
#plt.xlim(plt.xlim())
# plt.ylim(-1.5,0.5)
# plt.xlim(-1.2,0.5)
"""
plt.plot([crossing_point,crossing_point],[ymin,ymax],lw=0.5,c="black")
plt.plot([bare_pzc,bare_pzc],[ymin,ymax],c="royalblue",lw=1.5,zorder=0)
"""
plt.yticks(fontsize=14);plt.xticks(fontsize=14)
plt.ylabel("$\Omega$ [eV]",fontsize=16)
plt.xlabel("U vs. SHE [V]",fontsize=16)
plt.legend(frameon=False,markerfirst=False,fontsize=13,#loc="upper right",
           handletextpad=0.00,labelspacing=0.1) #,bbox_to_anchor=(1.08,1.03))

# plt.savefig("grand_potential.png",dpi=400,bbox_inches="tight",transparent=True)
plt.show()



