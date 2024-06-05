import numpy as np
import sys 
import matplotlib.pyplot as plt 
import pandas as pd 

files=sys.argv[1:]

data=dict()
for file in files: 
    with open(file) as f:
        lines=f.readlines()

    con=dict()
    for line in lines:
        tmp=line.split()
        tag=tmp[0].strip() 
        esol=float(tmp[-1])
        con[tag]=esol
    data[file]=con 

df=pd.DataFrame(data).T
print(df)

plt.figure(figsize=(8,4))
for col in df.columns : 
    y=df[col]
    plt.plot(np.arange(len(y)),y,marker="o",markersize=3, label=col )
plt.legend()
plt.show()


