#!/user/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa
import os
import time


rm = pyvisa.ResourceManager()  # 從 pyvisa 訪問 ni-visa
ins_tuples = rm.list_resources()  # 資料類型是 tuples
usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
rs232_ins = [i for i in ins_tuples if 'rs232' in i]
gpib_ins = [i for i in ins_tuples if 'GPIB' in i]
net_ins = [i for i in ins_tuples if 'TCPIP' in i]
print(rs232_ins)
if usb_ins:
    usb = rm.open_resource(usb_ins[0])
else:
    print('沒有連結USB')
    exit()
if gpib_ins:
    gpib = rm.open_resource(gpib_ins[0])
else:
    print('沒有連結GPIB')
if net_ins:
    net = rm.open_resource(net_ins[0])
else:
    print('沒有連結網路線')

sn = usb.query('Cal:sec:ser?')
sn = sn.strip('\n')
t = time.localtime()
test_folder_position = 'C:\\test_folder\\' + str(t.tm_year) + '\\' + \
                       str(t.tm_mon).zfill(2) + '\\' + str(t.tm_mday).zfill(2)

if os.path.isdir(test_folder_position):
    pass
else:
    os.system(f'md "{test_folder_position}"')
idn_usb = usb.query('*IDN?')
with open(test_folder_position + '\\' + sn + '.txt', 'w') as file:
    file.write('發送*IDN?\n\nUSB 連接測試\n')
    file.write(idn_usb)

if gpib_ins:
    idn_gpib = gpib.query('*IDN?')
    with open(test_folder_position + '\\' + sn + '.txt', 'a') as file:
        file.write('GPIB 連接測試\n')
        file.write(idn_gpib)
else:
    with open(test_folder_position + '\\' + sn + '.txt', 'a') as file:
        file.write('\nGPIB 沒有連接\n\n')

if net_ins:
    idn_net = net.query('*IDN?')
    with open(test_folder_position + '\\' + sn + '.txt', 'a') as file:
        file.write('TCP/IP 連接測試\n')
        file.write(idn_net)
else:
    with open(test_folder_position + '\\' + sn + '.txt', 'a') as file:
        file.write('\n網路線沒有連接\n\n')

os.system(f"""ping 192.168.1.253 >> {test_folder_position}\\{sn}.txt""")
input('\n按ENTER繼續\n')
os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" 192.168.1.253')
