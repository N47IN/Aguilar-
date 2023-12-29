"""Runs an XFOIL analysis for a given airfoil and flow conditions"""
import os
import subprocess
import numpy as np
import pandas as pd

airfoil_details=[]

def extract(a):
    params = []
    for i in range(len(a)):
        for j in range(len(a[i])):
         params.append(a[i][j][0:4])

def save_file(a,name):
   df = pd.DataFrame({"Name" : name, "AoA" : np.array(bb), "Cl": np.array(cc), "Cd": np.array(dd),"Cm": np.array(dd)})
   df.to_csv("diagnostics.csv", index=False)

def getProp():
    airfoil_name = "Aguilar"
    alpha_i = -0.50
    alpha_f = 0
    alpha_step = 0.25
    Re = 1000000
    n_iter = 1000

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
    print(r)

getProp()