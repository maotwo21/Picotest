import pyvisa
import time
import os

# 抓取有用到的USB port
rm = pyvisa.ResourceManager()  # 從pyvisa抓取
uut_tuples = rm.list_resources()  # 資料類型是tuples
uut_list = list(uut_tuples)  # 把資料類型改成list
# 啟用第X台uut
uut = rm.open_resource(uut_list[0])
idn = str(rm.open_resource(uut_list[0]))
idn = idn[39:-10]
# 檢查儀器是否連結
if len(idn) < 2:
    print('沒有USB儀器')
    os.system('pause')
    exit()
# 儀器序號
print('\n       目前連結的儀器為' + idn)
# 讀6次(1~6)寫7是因為最後一次沒送到
uut.write('ROUTe:SCAN:COUNT 7')
# 設定channel1~6為電阻
for i in range(6):
    uut.write(f'ROUTe:SCAN:FUNCtion {i+1},"RESistance"')
# 開始
uut.write('ROUTe:SCAN:STEP')
time.sleep(10)
# a為量測值
a = uut.query('FETCh?')
b = a.count(',')
c = 0
num_list = []
num_list2 = []
# 找出每個,的位置
for i in range(b):
    c = a.find(',', c+1)
    num_list += [c]
# 為了跑下面的for loop 要在num_list前面塞一個0
num_list = [0]+num_list
# 用每個,的位置找到中間的數值
for i in range(b):
    d = a[num_list[i]+1:num_list[i+1]]
    num_list2 += [d]
print(num_list2)
# 判斷是否在範圍內
if 3100 < float(num_list2[0]) < 4100:
    print('+3.3V  pass')
if 3900 < float(num_list2[1]) < 4900:
    print('VSS1   pass')
if 7100 < float(num_list2[2]) < 8100:
    print('+3.3VA pass')
if 800 < float(num_list2[3]) < 1800:
    print('VDD5   pass')
if 1800 < float(num_list2[4]) < 2800:
    print('VDD1   pass')
if 10800 < float(num_list2[5]) < 11800:
    print('+7VREF pass')

print('\n      電阻量測完畢，請開啟電源\n')
os.system('pause')

# 設定channel1~6為DCV
for i in range(6):
    uut.write(f'ROUTe:SCAN:FUNCtion {i+1},"VOLT:DC"')
uut.write('ROUTe:SCAN:STEP')
time.sleep(10)
# a為量測值
a = uut.query('FETCh?')
b = a.count(',')
c = 0
num_list = []
num_list2 = []
# 找出每個,的位置
for i in range(b):
    c = a.find(',', c+1)
    num_list += [c]
# 為了跑下面的for loop 要在num_list前面塞一個0
num_list = [0]+num_list
# 用每個,的位置找到中間的數值
for i in range(b):
    d = a[num_list[i]+1:num_list[i+1]]
    num_list2 += [d]
print(num_list2)
if 3.2144 < float(num_list2[0]) < 3.3456:
    print('+3.3V  pass')
if -18.54 < float(num_list2[1]) < -17.46:
    print('VSS1   pass')
if 3.2472 < float(num_list2[2]) < 3.3128:
    print('+3.3VA pass')
if 5.145 < float(num_list2[3]) < 5.355:
    print('VDD5   pass')
if 17.46 < float(num_list2[4]) < 18.54:
    print('VDD1   pass')
if 6.6025 < float(num_list2[5]) < 7.2975:
    print('+7VREF pass')
os.system('pause')
