#!/user/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa
import os
import time


rm = pyvisa.ResourceManager()  # 從 pyvisa 訪問 ni-visa
ins_tuples = rm.list_resources()  # 資料類型是 tuples
usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
rs232_ins = [i for i in ins_tuples if 'ASRL1:' in i]
gpib_ins = [i for i in ins_tuples if 'GPIB' in i]
net_ins = [i for i in ins_tuples if 'TCPIP' in i]

if usb_ins:
    usb = rm.open_resource(usb_ins[0])
if rs232_ins:
    rs232 = rm.open_resource(rs232_ins[0])
if gpib_ins:
    gpib = rm.open_resource(gpib_ins[0])
if net_ins:
    net = rm.open_resource(net_ins[0])
try:
    sn = usb.query('Cal:sec:ser?')
    sn_usb = sn.strip('\n')
except:
    pass
try:
    sn = rs232.query('Cal:sec:ser?')
    sn_rs232 = sn.strip('\n')
except:
    pass
try:
    sn = gpib.query('Cal:sec:ser?')
    sn_gpib = sn.strip('\n')
except:
    pass
try:
    sn = net.query('Cal:sec:ser?')
    sn_net = sn.strip('\n')
except:
    pass

t = time.localtime()
test_folder_position = 'C:\\test_folder\\' + str(t.tm_year) + '\\' + \
                       str(t.tm_mon).zfill(2) + '\\' + str(t.tm_mday).zfill(2)

if os.path.isdir(test_folder_position):
    pass
else:
    os.system(f'md "{test_folder_position}"')

if usb_ins:
    idn_usb = usb.query('*IDN?')
    with open(test_folder_position + '\\' + sn_usb + '.txt', 'w') as file:
        file.write('發送*IDN?\n\nUSB 連接測試\n')
        file.write(idn_usb)
    print('USB 連接成功')
elif gpib_ins:
    with open(test_folder_position + '\\' + sn_gpib + '.txt', 'a') as file:
        file.write('\nUSB 沒有連接\n\n')
        input('USB 沒有連接  按Enter繼續')
else:
    with open(test_folder_position + '\\' + sn_rs232 + '.txt', 'a') as file:
        file.write('\nUSB 沒有連接\n\n')
        input('USB 沒有連接  按Enter繼續')

if gpib_ins:
    idn_gpib = gpib.query('*IDN?')
    with open(test_folder_position + '\\' + sn_gpib + '.txt', 'a') as file:
        file.write('GPIB 連接測試\n')
        file.write(idn_gpib)
    print('GPIB 連接成功')
elif usb_ins:
    with open(test_folder_position + '\\' + sn_usb + '.txt', 'a') as file:
        file.write('\nGPIB 沒有連接\n\n')
        input('GPIB 沒有連接  按Enter繼續')
else:
    with open(test_folder_position + '\\' + sn_rs232 + '.txt', 'a') as file:
        file.write('\nGPIB 沒有連接\n\n')
        input('GPIB 沒有連接  按Enter繼續')


if rs232_ins:
    try:
        idn_rs232 = rs232.query('*IDN?')

    except:
        if usb_ins:
            with open(test_folder_position + '\\' + sn_usb + '.txt', 'a') as file:
                file.write('\nRS232沒有連接\n\n')
                input('RS232沒有連接  按Enter繼續')
        elif gpib_ins:
            with open(test_folder_position + '\\' + sn_gpib + '.txt', 'a') as file:
                file.write('\nRS232沒有連接\n\n')
                input('RS232沒有連接  按Enter繼續')
    else:
        with open(test_folder_position + '\\' + sn_rs232 + '.txt', 'w') as file:
            file.write('RS232 連接測試\n')
            file.write(idn_rs232)
        print('RS232連接成功')

if net_ins:
    idn_net = net.query('*IDN?')
    with open(test_folder_position + '\\' + sn_net + '.txt', 'a') as file:
        file.write('TCP/IP 連接測試\n')
        file.write(idn_net)
    print('網路線連接成功')
    os.system(f"""ping 192.168.1.253 >> {test_folder_position}\\{sn_net}.txt""")
    os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" 192.168.1.253')

else:
    with open(test_folder_position + '\\' + sn_usb + '.txt', 'a') as file:
        file.write('\n網路線沒有連接\n\n')
        input('網路線沒有連接  按Enter繼續')

print('測試結束')
input(f'測試結果存在{test_folder_position}\\{sn_usb}')
