import numpy as np 
from ase.io import read 
from ase.visualize import view
import sys 
import re

"""
python view_from_dynmat.py scf.in dynmat.mold 7 8 9
"""

structurefile=sys.argv[1]
modefile=sys.argv[2]
nummodes=[int(i) for i in sys.argv[3:]]

# ------------------------------ read dynmat.mold
with open(modefile) as f:
    data=f.read() 
start_index_for_pattern=[]; pattern = "vibration"
for match in re.finditer(pattern, data):
    start_index_for_pattern.append(match.start())
N = len(start_index_for_pattern); modes = []
for ind in range(N) :
    if ind == N-1 :
        phrase = data[start_index_for_pattern[ind]:]
    else :
        phrase = data[start_index_for_pattern[ind]:start_index_for_pattern[ind+1]]
    mode_i = [[float(k) for k in tmplist.strip().split()] for tmplist in phrase.split("\n")[1:4]]
    modes.append(mode_i)
modes=np.array(modes)

# -------------------------------- set mode 
steps = 40;maxstep = 0.2
atoms = read(structurefile); view_structures = []
factors = np.linspace(-maxstep, maxstep, steps, endpoint=True)
for nummode in nummodes :
    vector = modes[nummode-1]
    for factor in factors:
        atoms_shifted=atoms.copy()
        position_shifted=atoms_shifted.positions
        position_shifted+=factor*vector
        atoms_shifted.set_positions(position_shifted)
        view_structures.append(atoms_shifted)

# -------------------------------- view mode 
view(view_structures)









