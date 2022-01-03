# run in custom environment with the required packages

import numpy as np

# defining parameters
gm1 = 2e-3
r1  = 500e3
c1  = 0.6e-12
cc  = 12.5e-12
gm2 = 5e-3
r2  = 20e3
c2  = 0.8e-12

filename = "dummy.cir"
with open(filename,"r") as file:
    lines = file.readlines()

for i in lines:
    print(i,end="")
