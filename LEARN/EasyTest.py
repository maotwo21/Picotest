import pyvisa
from time import sleep
import os

# looking the USB instrument port
rm = pyvisa.ResourceManager()
print(rm.list_resources())  # 資料類型是tuples

# delimit instrument's name
dmm = rm.open_resource('USB0::0x164E::0x0DB6::TW00011204::INSTR')
supply = rm.open_resource('USB0::0x164E::0x258A::TW00036148::INSTR')

# setting datafile name
filepath = "UUT data/data.csv"

# setup Digital MultiMeter in DC 10 Voltage mode
dmm.write('CONFigure:VOLTage:DC 10')

# setup the power supply 5V
supply.write('outp 0')  # supply OFF
supply.write('Volt 0')  # apply 0v

# Run the test
supply.write('outp 1')
v = 0
while v < 5.0:
    supply.write('Volt ' + str(v))
    sleep(2)
    vMeasured = float(dmm.query('read?'))

    # Write results to console
    print("{} {}".format(v, vMeasured))

    # Write result to a file
    with open(filepath, "a") as file:
        if os.stat(filepath).st_size == 0:  # if empty file, write a nice header
            file.write("Setpoint [V], Measured [V]\n")
        file.write("{:12.7f},{:13.7f}\n".format(v, vMeasured))

    v += 0.5

# Test complete
supply.write('outp 0')
supply.write('Volt 0')
