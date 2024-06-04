from ase.io import read 
import sys 

filename=sys.argv[1]
Npoints=int(sys.argv[2])

atoms=read(filename)
kpath=atoms.cell.bandpath("GXWLGK",npoints=Npoints)

print("K_POINTS crystal_b")
print(len(kpath.kpts))
for line in kpath.kpts : 
    print(" {:8.6f}  {:8.6f}  {:8.6f}  {:4.3f}".format(line[0],line[1],line[2],1))




