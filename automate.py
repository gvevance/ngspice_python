# run in custom environment with the required packages
# TODO: Add an interactive mode for the circuit

import numpy as np
from subprocess import call

# defining parameters
gm1 = 2e-3
r1  = 500e3
c1  = 0.6e-12
cc  = 12.5e-12
gm2 = 5e-3
r2  = 20e3
c2  = 0.8e-12

filename = "dummy.cir"

contents = f'''2 stage OTA. Final aim - use RL agent to design it

* Circuit definition
vin 1 0 dc 0 ac 1
gm1 2 0 1 0 -{gm1}
r1 2 0 {r1}
c1 2 0 {c1}
cc 2 3 {cc}
gm2 3 0 2 0 {gm2}
r2 3 0 {r2}
c2 3 0 {c2}

*****************************************
* Control block
*****************************************
.control

*****************************************
* Analysis command
*****************************************
ac dec 10 1e-3 10G

*****************************************
* Measuring performance metrics 
*****************************************

* measuring phase margin
let vp_deg = vp(3)*57.29
meas ac phase_margin 
+ FIND vp_deg WHEN vdb(3) = 0

* measuring DC gain
meas ac DC_gain_dB
+ MAX vdb(3) from=1e-3 to=10G 

* measuring UGF
meas ac UGF
+ WHEN vdb(3)=0 CROSS=1

*****************************************
* Bode plots of vout 
*****************************************

* Magnitude dB plot for v(3) on log scale
*plot vdb(3) xlog
*+ xlabel 'Frequency in Hz'
*+ ylabel 'Magnitude in dB'
*+ title 'Magnitude plot'

* Phase in degrees plot for v(3) on log scale
*plot {{57.29*vp(3)}} xlog
*+ xlabel 'Frequency in Hz'
*+ ylabel 'Phase in deg'
*+ title 'Phase plot'

*****************************************
* Output measured values into output.csv 
*****************************************
echo "$&DC_gain_dB $&UGF $&phase_margin" >> output.csv

*****************************************
* Run
*****************************************
run

exit ; so that ngspice does not end in interactive mode

.endc
.end
'''

# print(string1)
with open(filename,"w") as file:
    file.write(contents)

call(["ngspice", "dummy.cir"])
