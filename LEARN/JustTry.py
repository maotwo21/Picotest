import pyvisa
import os
import time


class ConnectedUUT:
    def __init__(self):
        rm = pyvisa.ResourceManager()  # 從pyvisa抓取
        ins_tuples = rm.list_resources()  # 資料類型是tuples
        usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
        gpib_ins = [i for i in ins_tuples if 'GPIB' in i]
        # 確定只有一台使用USB的儀器(電供不算)後，建立連結與id捷徑
        if len(usb_ins) == 1:
            self.ins = rm.open_resource(usb_ins[0])
            self.gpib = rm.open_resource(gpib_ins[0])
        else:
            print('"Meter" 的數量不是一台!(沒插usb OR 連結2台以上的meter)')
            os.system('pause')


def stats():
    stat = a.ins.query('CAL:PROT:STAT?')
    while stat != stat_ok:
        stat = a.ins.query('CAL:PROT:STAT?')
        time.sleep(1)


def sre():
    isr = a.gpib.query('ISR?')
    while isr != isr_ok:
        isr = a.gpib.query('ISR?')
        time.sleep(1)


def save():
    a.ins.write('CAL:PROT:SAVE')
    a.ins.write('CAL:PROT:LOCK')
    a.ins.write('*RST')
    sec = time.time()
    struct_time = time.localtime(sec)
    date = time.strftime("%m/%d/%Y", struct_time)
    a.ins.write(f'CAL:PROT:DATE "{date}"')
    if '2110' in idn:
        a.ins.write('CAL:COUN:BACK:ZERO')


def unlock():
    if '2110' in idn:
        a.ins.write('CAL:PROT:CODE 123456')
        a.ins.write('CAL:PROT:INIT')


a = ConnectedUUT()
a.ins.write('*CLS')
a.ins.write('*RST')
idn = a.ins.query('*IDN?')
print(idn)
stat_ok = a.ins.query('CAL:PROT:STAT?')

unlock()
# 校正ZERO
"""
a.ins.write('CONF:VOLT:DC')
a.ins.write('CAL:PROT:DC:STEP 3,0')
stats()

a.ins.write('CONF:TCO')
a.ins.write('CAL:PROT:DC:STEP 3,0')
stats()
"""
print('電容 zero，拔除 short pin & tcoup short pin.')
os.system('pause')

a.ins.write('CONF:CAP')
a.ins.write('CAL:PROT:DC:STEP 3,0')
stats()
"""
save()

"""
# 校正電容
print('電容校驗，連結 5520 normal 與 3510 input.')
os.system('pause')

a.gpib.write('*CLS;*SRE 8;*ESE 1')
a.gpib.write(f'ZCOMP NONE;OUT 2e-10F;OPER;*OPC')
time.sleep(3)
isr_ok = a.gpib.query('ISR?')
print(isr_ok)
a.gpib.write('*CLS;*RST;*SRE 8;*ESE 1;*OPC')
a.gpib.write('UUT_FLUSH')
os.system('pause')


model = a.gpib.query('*IDN?')
if '5520' in model:
    output = 0.2
    print(output)
elif '5522' in model:
    output = 0.22
    print(output)
else:
    output = 0
    print('沒找到 5520 或 5522')
    os.system('pause')
    exit()

# 1e-9
a.ins.write('CONF:CAP 1E-9')
a.ins.write('AVERAGE:STATE OFF')
a.gpib.write('*CLS;*SRE 8;*ESE 1')
a.gpib.write(f'ZCOMP NONE;OUT {output}e-9F;OPER;*OPC')
sre()
a.ins.write(f'CAL:PROT:DC:STEP 1,{output}e-9')
stats()
a.gpib.write('*CLS;*SRE 8;*ESE 1')
a.gpib.write('ZCOMP NONE;OUT 1e-9F;OPER;*OPC')
sre()
a.ins.write('CAL:PROT:DC:STEP 2,1e-09')
stats()

x = 8
y = [1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 110e-6, 1e-3, 10e-3]
for i in range(7):
    a.ins.write(f'CONF:CAP 1E-{x}')
    x -= 1
    a.ins.write(f'CAL:PROT:DC:STEP 1,{y[i]}')
    stats()
    a.gpib.write('*CLS;*SRE 8;*ESE 1')
    a.gpib.write(f'ZCOMP NONE;OUT {y[i+1]}F;OPER;*OPC')
    sre()
    a.ins.write(f'CAL:PROT:DC:STEP 2,{y[i+1]}')
    stats()

a.gpib.write('*CLS;*RST;*SRE 8;*ESE 1;*OPC')
a.gpib.write('UUT_FLUSH')

# 校正熱電偶

print('熱電偶校驗，連結 5520 TC 與 3510 TC input.')
os.system('pause')
