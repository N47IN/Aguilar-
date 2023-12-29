"""Runs an XFOIL analysis for a given airfoil and flow conditions"""
import os
import subprocess
import numpy as np
import pandas as pd
a=[]
b=[]
c=[]
d=[]
e=[]

airfoil_details=[]

def extract(a):
    params = []
    for i in range(len(a)):
        for j in range(len(a[i])):
         params.append(a[i][j][0:4])


def save_file(aa,bb,cc,dd,ee):
   df = pd.DataFrame({"Name" : np.array(aa), "AoA" : np.array(bb), "Cl": np.array(cc), "Cd": np.array(dd),"Cm": np.array(ee)})
   df.to_csv("output.csv", index=False)

def getProp(i):
    global a
    global b
    global c
    global d
    global e
    airfoil_name = f'{i}'
    alpha_i = -10
    alpha_f = 10
    alpha_step = 1
    Re = 1000000
    n_iter = 100

    if os.path.exists("polar_file.txt"):
     os.remove("polar_file.txt")

    input_file = open("input_file.in", 'w')
    t=input_file.write("LOAD {0}.dat\n".format(airfoil_name))
    input_file.write(airfoil_name + '\n')
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
                                             alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")
    input_file.close()
    
    subprocess.call("xfoil.exe < input_file.in", shell=True)
    polar_data = np.loadtxt("polar_file.txt", skiprows=12)
    r=[(airfoil_name,k[0:4]) for  k in polar_data]
    for i in range(20):
       
       a.append(r[i][0])
       b.append(r[i][1])
       c.append(r[i][2])
       d.append(r[i][3])
       e.append(r[i][4])
    save_file(a,b,c,d,e)

for i in range(1,150):
 getProp(i)