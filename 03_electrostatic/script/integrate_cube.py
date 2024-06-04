import numpy as np
import matplotlib.pyplot as plt 
import sys 

filenames=sys.argv[1:-1]
int_axis=sys.argv[-1]

plotgraph = True

class readcube():

    def __init__(self,filename):
        self.filename=filename
        self.loaddata()
    
    def loaddata(self):
        with open(self.filename) as f:
            f.readline()
            f.readline()
            nat=int(f.readline().split()[0])
            print("number of atoms     : ", nat )
            linex=f.readline().split()
            liney=f.readline().split()
            linez=f.readline().split()
            self.Nx=int(linex[0])
            self.Ny=int(liney[0])
            self.Nz=int(linez[0])
            self.vec_x=[float(i) for i in linex[1:]]
            self.vec_y=[float(i) for i in liney[1:]]
            self.vec_z=[float(i) for i in linez[1:]]
            atomic_numbers=[]
            positions=[]
            for inat in range(nat) :
                tmp=f.readline().split()
                atomic_numbers.append(int(tmp[0]))
                positions.append([float(i) for i in tmp[2:]])
            print("atomic numbers      : ", atomic_numbers)
            self.positions = np.array(positions)
            self.atomic_numbers = atomic_numbers

            N_vol_lines=int(self.Nx*self.Ny*self.Nz/6)
            volmetric=[]
            for iline in range(N_vol_lines):
                line=f.readline().split()
                volmetric+=[float(i) for i in line]
            print("grid Nx, Ny, Nz     : ", self.Nx, self.Ny, self.Nz)
            print("total mesh          : ", self.Nx*self.Ny*self.Nz)
            self.volmetric=np.array(volmetric).reshape(self.Nx,self.Ny,self.Nz) 

    def integrate_along(self,int_axis,fileout=True,unit="Angs"):

        if unit=="Angs":
            fac = 0.529177
        elif unit == "au":
            fac=1.0
        else: 
            fac=1.0

        print("integrate along     :  {}".format(int_axis))

        if int_axis == "a":
            self.avg=self.volmetric.sum(axis=2).sum(axis=1) / self.Nz / self.Ny
            self.axis_line=np.arange(1,len(self.avg)+1)*np.linalg.norm(self.vec_x)*fac
            self.positions = self.positions * fac ; self.tag=0
        elif int_axis == "b":
            self.avg=self.volmetric.sum(axis=2).sum(axis=0) / self.Nz / self.Nx
            self.axis_line=np.arange(1,len(self.avg)+1)*np.linalg.norm(self.vec_y)*fac
            self.positions = self.positions * fac ; self.tag=1
        elif int_axis == "c":
            self.avg=self.volmetric.sum(axis=1).sum(axis=0) / self.Ny / self.Nx
            self.axis_line=np.arange(1,len(self.avg)+1)*np.linalg.norm(self.vec_z)*fac
            self.positions = self.positions * fac ; self.tag=2

        if fileout:
            # fileoutname="planar_average.dat".format(int_axis)
            fileoutname="{}.{}.avg".format(self.filename,int_axis)
            with open(fileoutname,"w") as fileout:
                fileout.write("#     axis        intval\n")
                for _i, _j in zip(self.axis_line,self.avg):
                    fileout.write("{:12.8f}  {:12.8f}\n".format(_i,_j))
            print("saved to file       : {}".format(fileoutname))


if plotgraph :
    fig=plt.figure(figsize=(8,4))
    colors = ["firebrick","dodgerblue","forestgreen","dimgray"]

for count,filename in enumerate(filenames):
    
    print( " --- reading # {}".format(count))

    #--------------------------- load data
    cubedata=readcube(filename=filename)
    cubedata.integrate_along(int_axis,unit="Angs")

    #--------------------------- plot graph
    xmin, xmax = cubedata.axis_line.min(),cubedata.axis_line.max()
    plt.plot(cubedata.axis_line,cubedata.avg,c=colors[count],label=filename)
    for pos in cubedata.positions :
        plt.scatter(pos[cubedata.tag],0,facecolors="black",edgecolors="black",
                    s=cubedata.axis_line.max()*10,alpha=0.2)

    plt.plot([xmin, xmax],[0,0],lw=0.5,c='black')
    plt.xlabel("{} axis ".format(int_axis) + "[$\AA$]", fontsize=14)
    plt.ylabel("$\int \\rho (\\vec{r}) dS$",fontsize=14)
    plt.xticks(fontsize=14);plt.yticks(fontsize=14)
    plt.xlim(xmin, xmax)
    plt.legend(frameon=False,markerfirst=False)
    plt.tight_layout()


if plotgraph :
    plt.show()

