import argparse
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import integrate

parser=argparse.ArgumentParser()
parser.add_argument("-inp")
parser.add_argument("-rho")
parser.add_argument("-col")
parser.add_argument("-range")
args=parser.parse_args()

#---------------------------------------------------------- input parameters 

l_int        = True
filename     = args.inp
print("correlation function from 1D-RISM was read from   : ",filename)


if args.rho :
    rho = float(args.rho)
    print( "INPUT rho                                         : ", rho)
else :
    rho          = 0.49533751E-02  # default for water 
    print( "NO input rho and defalut value will be used       : ", rho)


if args.col :
    column       = args.col
    print( "INPUT col                                         : ", column)
else :
    column       = 'O/h2o:O/h3o'
    print( "NO input col and defalut value will be used       : ", column)


if args.range :
    phrase=args.range.split(",")
    x_min = float(phrase[0])
    x_max = float(phrase[1])
    print( "INPUT range                                       : ", x_min , x_max )
else :
    x_min, x_max = 0,3.8
    print( "NO input col and defalut value will be used       : ", x_min , x_max )



#---------------------------------------------------------- function for reading 1D-RISM data 
def read_1drism(filename):
    with open(filename) as f :
        lines=f.readlines()
    tags=lines[4].strip().split()
    gvv=np.array([ [ float(com) for com in line.split()] for line in lines[5:]]).T
    # gvv = np.loadtxt( filename, comments='#', skiprows = 5 )
    gvv_dict=dict(zip(tags,gvv))
    return gvv_dict

#---------------------------------------------------------- initialization of variables

gvv_dict      = read_1drism(filename)
r_dist        = gvv_dict['r/Angstrom']
gvv_func      = gvv_dict[column]
bohr_to_angst = 0.529177
rho           = rho/(bohr_to_angst**3)
x             = r_dist
y             = gvv_func
y_int         = [0]
Nx            = len(r_dist)

#----------------------------------------------- the integration of the correlation function 

frac          = np.zeros_like(x)
frac[np.where((x > x_min) & (x < x_max))]=1
for i in range( 1, Nx ):
    sub_y=4.0*np.pi*x[0:i]*x[0:i]*rho*y[0:i]*frac[0:i]
    # sub_int=integrate.simpson(sub_y, x[0:i])
    sub_int=integrate.trapezoid(sub_y, x[0:i])  # somehow more stable (numerically)
    y_int.append(sub_int)
coord_num=y_int[-1]

if l_int :
    print("integrate from                                    : {} to {}".format(x_min,x_max))
    print("the coordination number is                        : {}".format(coord_num))
else:
    print("NO integration")


#---------------------------------------------------------- plotting 
fig,ax=plt.subplots(figsize=(5,4))
ax.plot(x,y,lw=1.0,c="black")
ax.plot([0,x[-1]],[0,0],lw=1.0,c="black")
plt.xlim(0,10)
ax.set_ylabel("g(r)",fontsize=14)
ax.set_xlabel("r [$\AA$]",fontsize=14)

if l_int:
    ax.fill_between(x,y,0,where=(x>x_min) & (x<=x_max),color="orange")
    ax2=ax.twinx()
    ax2.plot(x,y_int,lw=2.0,c="firebrick",alpha=0.5)
    ax2.set_ylabel("CN",fontsize=14)
    ax2.text(plt.xlim()[1]*0.7,coord_num*0.9,"CN : {:4.2f}".format(coord_num),fontsize=14)

plt.title(column,fontsize=14)
plt.tight_layout()
plt.show()


print("------------------------------")
print("tags for interaction pairs : ")
print(gvv_dict.keys())







