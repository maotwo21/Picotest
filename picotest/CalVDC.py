import pyvisa
import time
import os

# 抓取有用到的USB port
rm = pyvisa.ResourceManager()  # 從pyvisa抓取
uut_tuples = rm.list_resources()  # 資料類型是tuples
uut_list = list(uut_tuples)  # 把資料類型改成list
# 啟用第X台uut
uut = rm.open_resource(uut_list[0])
calibrator = rm.open_resource(uut_list[-2])
print(uut_list)
idn = str(rm.open_resource(uut_list[0]))
idn = idn[39:-10]

# 檢查儀器是否連結
if len(idn) < 2:
    print('沒有USB儀器')
    os.system('pause')
    exit()
# 儀器序號
print('\n\n\n       目前連結的儀器為' + idn)

# 判斷UUT是 2110 OR 3510
if len(idn) == 8:
    uut.write('cal:prot:code 123456;init')
    lock = uut.query('cal:prot:lock?')
    if lock < 0:
        print('      沒有解鎖成功\n      請重試')
        os.system('pause')
        exit()

# uut檔位
uut.write('conf:volt:DC 10')
uut.write('volt:nplc 10')
# 讀5700輸出數值
calibrator.write('out 0V ; OPER')
time.sleep(2)

uut.write('CAL:PROT:DC:STEP 1,0')
time.sleep(6)

calibrator.write('out 10V ; OPER')
time.sleep(2)
a = calibrator.query('out?')

uut.write(f'CAL:PROT:DC:STEP 2,{a}')
time.sleep(6)

calibrator.write('out -10V ; OPER')
time.sleep(2)
a = calibrator.query('out?')

uut.write(f'CAL:PROT:DC:STEP 2,{a}')
time.sleep(6)

calibrator.write('STBY')

date = input('\n       請輸入校正日期\n')
uut.write('CAL:PROT:SAVE')
uut.write('CAL:PROT:LOCK')
uut.write('*RST')
uut.write('CAL:PROT:DATE ' + '"' + date + '"')
print('\n      日期為', date)
