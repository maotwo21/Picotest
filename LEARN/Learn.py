import pyvisa
import os
import time


class ConnectedUUT:  # 連接快捷
    def __init__(self):
        rm = pyvisa.ResourceManager()  # 從pyvisa抓取
        ins_tuples = rm.list_resources()  # 資料類型是tuples
        usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
        gpib_ins = [i for i in ins_tuples if 'GPIB' in i]
        # 確定只有一台使用USB的儀器(電供不算)後，建立連結與id捷徑
        if len(usb_ins) == 1 & len(gpib_ins) == 1:
            self.ins = rm.open_resource(usb_ins[0])
            self.gpib = rm.open_resource(gpib_ins[0])
        else:
            print('"Meter" 的數量不是一台!(沒插usb OR 連結2台以上的meter)')
            os.system('pause')


class Colors:  # 字體顏色
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def stats():  # DMM狀態
    stat = a.ins.query('CAL:PROT:STAT?')
    while stat != stat_ok:
        stat = a.ins.query('CAL:PROT:STAT?')
        time.sleep(1)


def sre():  # Calibrator狀態
    isr = a.gpib.query('ISR?')
    while isr != isr_ok:
        isr = a.gpib.query('ISR?')
        time.sleep(1)


def save():  # DMM儲存校正值(日期)
    a.ins.write('CAL:PROT:SAVE')
    a.ins.write('CAL:PROT:LOCK')
    a.ins.write('*RST')
    sec = time.time()
    struct_time = time.localtime(sec)
    date = time.strftime("%m/%d/%Y", struct_time)
    a.ins.write(f'CAL:PROT:DATE "{date}"')
    if '2110' in idn:
        a.ins.write('CAL:COUN:BACK:ZERO')


def unlock():  # 校正解鎖密碼
    if '2110' in idn:
        a.ins.write('CAL:PROT:CODE 123456')
        a.ins.write('CAL:PROT:INIT')


def reset():  # Calibrator重置
    a.gpib.write('*CLS;*RST;*SRE 8;*ESE 1;*OPC')
    a.gpib.write('UUT_FLUSH')


def cal_zero():  # 自身ZERO校正
    unlock()
    print('插入 short pin & tcoup short pin.')
    os.system('pause')
    os.system('cls')
    a.ins.write('CONF:VOLT:DC')
    a.ins.write('CAL:PROT:DC:STEP 3,0')
    stats()
    a.ins.write('CONF:TCO')
    a.ins.write('CAL:PROT:DC:STEP 3,0')
    stats()

    print('拔除 short pin & tcoup short pin.')
    os.system('pause')
    os.system('cls')
    a.ins.write('CONF:CAP')
    a.ins.write('CAL:PROT:DC:STEP 3,0')
    stats()
    save()


def cal_cap():
    # 校正電容
    unlock()
    print('連結 5520 normal 與 3510 input.')
    os.system('pause')
    os.system('cls')
    model = a.gpib.query('*IDN?')
    if '5520' in model:
        output = 0.2
    elif '5522' in model:
        output = 0.22
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
    reset()
    save()


def cal_tco():
    # 校正熱電偶
    unlock()
    x = [1, 2, 2]
    y = [0, 0.1, -0.1]
    a.ins.write(f'CONF:VOLT:DC 0.1')
    for i in range(3):
        a.gpib.write('*CLS;*SRE 8;*ESE 1')
        a.gpib.write(f'OUT {y[i]}V,0 Hz;EARTH OPEN;EXTGUARD OFF;OPER;*OPC')
        sre()
        a.ins.write(f'CAL:PROT:DC:STEP {x[i]},{y[i]}')
        stats()
    x = [1, 2]
    y = [0, 1]
    a.ins.write('CONF:VOLT:DC 1')
    for i in range(2):
        a.gpib.write('*CLS;*SRE 8;*ESE 1')
        a.gpib.write(f'OUT {y[i]}V,0Hz;EARTH OPEN;EXTGUARD OFF;OPER;*OPC')
        sre()
        a.ins.write(f'CAL:PROT:DC:STEP {x[i]},{y[i]}')
        stats()
    reset()
    print('連結 5520 TC 與 3510 TC input(要拔除3510 input.')
    os.system('pause')
    os.system('cls')
    a.ins.write('CONF:TCO')
    a.gpib.write('*CLS;*SRE 8;*ESE 1')
    a.gpib.write('TSENS_TYPE TC;TC_TYPE K;TC_REF INT;OUT 0cel;OPER;*OPC')
    sre()
    time.sleep(300)
    a.ins.write('CAL:PROT:DC:STEP 1,0')
    stats()
    reset()
    save()


def vef_tco():
    # 驗證熱電偶
    t_coup_desc = ['0 degC @ TCOUPL_TYPE_K', '50 degC @ TCOUPL_TYPE_K', '500 degC @ TCOUPL_TYPE_K',
                   '1000 degC @ TCOUPL_TYPE_K', '1372 degC @ TCOUPL_TYPE_K', '-200 degC @ TCOUPL_TYPE_K']  # 測試名稱
    deg_lower = [-0.500000, 49.500000, 499.500000, 999.500000, 1371.500000, -200.500000]
    deg_upper = [0.500000, 50.500000, 500.500000, 1000.500000, 1372.500000, -199.500000]
    tc = [0, 50, 500, 1000, 1372, -200]
    cel = []
    a.ins.write('CONF:TCO')
    for i in range(6):
        status = 'pass'
        a.gpib.write('*CLS;*SRE 8;*ESE 1')
        a.gpib.write(f'TSENS_TYPE TC;TC_TYPE K;TC_REF INT;OUT {tc[i]}cel;OPER;*OPC')
        sre()
        cel.append(float(a.ins.query('READ?')))
        stats()
        if deg_lower[i] > cel[i] or deg_upper[i] < cel[i]:
            status = 'fail'
            print(Colors.FAIL +
                  f'{t_coup_desc[i]}    {cel[i]}    {deg_lower[i]}    {deg_upper[i]}    {status}'
                  + Colors.RESET)
            os.system('pause')
        else:
            print(f'{t_coup_desc[i]}    {cel[i]}    {deg_lower[i]}    {deg_upper[i]}    {status}')


def vef_cap():
    print('拔除 5520 normal(3510 input 需插著)')
    os.system('pause')
    os.system('cls')
    # 1nF的NULL值
    a.ins.write(f'CONF:CAP 1e-9')
    a.ins.write('SAMP:COUN 20')
    a.ins.write('CALC:FUNC AVER')
    a.ins.write('CALC:STAT 1')
    a.ins.query('READ?')
    null_max = a.ins.query('CALC:AVER:MAX?')
    null_min = a.ins.query('CALC:AVER:MIN?')
    null_1nf = (null_max+null_min)/2
    # 1uF到10mF的NULL值
    a.ins.write('SAMP:COUN 1')
    a.ins.write('CALC:STAT 0')
    cap = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    null = []
    for i in range(5):
        a.ins.write(f'CONF:CAP {cap[i]}')
        a.ins.write('SAMP:COUN 20')
        a.ins.write('CALC:FUNC AVER')
        a.ins.write('CALC:STAT 1')
        a.ins.query('READ?')
        null_max = a.ins.query('CALC:AVER:MAX?')
        null_min = a.ins.query('CALC:AVER:MIN?')
        null.append((null_max + null_min) / 2)
        a.ins.write('SAMP:COUN 1')
        a.ins.write('CALC:STAT 0')
    # 1nF的讀值
    cap1 = []
    a.ins.write('CONF:CAP 1E-9')
    a.ins.write('CALC:FUNC NULL')
    a.ins.write('CALC:STATE ON')
    a.ins.query('READ?')
    a.ins.write(f'CALC:NULL:OFFS {null_1nf}')
    a.gpib.write('*CLS;*SRE 8;*ESE 1')
    a.gpib.write(f'ZCOMP NONE;OUT 1e-9F;OPER;*OPC')
    cap1.append(a.ins.query('READ?'))
    # 10、100nF的讀值
    x = [1e-8, 1e-7]
    for i in range(2):
        a.ins.write(f'SENS:CAP:RANG {x[i]}')
        a.gpib.write('*CLS;*SRE 8;*ESE 1')
        a.gpib.write(f'ZCOMP NONE;OUT {x[i]}F;OPER;*OPC')
        cap1.append(a.ins.query('READ?'))
    # 1uF的讀值
    a.ins.write('CALC:STATE OFF')
    a.ins.write(f'SENS:CAP:RANG {cap[0]}')
    a.ins.write('CALC:FUNC NULL')
    a.ins.write('CALC:STATE ON')
    a.ins.write(f'CALC:NULL:OFFS {null[0]}')
    a.gpib.write('*CLS;*SRE 8;*ESE 1')
    a.gpib.write(f'ZCOMP NONE;OUT {cap[0]}F;OPER;*OPC')
    cap1.append(a.ins.query('READ?'))
    # 10uF到10mF的讀值
    cap2 = []
    for i in range(4):
        a.ins.write('CALC:STATE OFF')
        a.ins.write(f'SENS:CAP:RANG {cap[i+1]}')
        a.ins.write('CALC:FUNC NULL')
        a.ins.write('CALC:STATE ON')
        a.ins.write(f'CALC:NULL:OFFS {null[i+1]}')
        a.gpib.write('*CLS;*SRE 8;*ESE 1')
        a.gpib.write(f'ZCOMP NONE;OUT {cap[i+1]}F;OPER;*OPC')
        cap2.append(a.ins.query('READ?'))
    a.ins.write('CALC:STATE OFF')
    reset()
    a.ins.write('*RST')
    # 檢驗數值是否在範圍內
    cap1_desc = [' 1 nF @ CAP 1nf', ' 10 nF @ CAP 1nf', ' 100 nF @ CAP 1nf', ' 1 uF @ CAP 1uf']
    cap2_desc = [' 10 uF @ CAP 10uf', ' 110 uF @ CAP 100uf', ' 1 mF @ CAP_1mf', ' 10 mF @ CAP_10mf']
    cap1s_lower = [0.986000, 0.986000, 99.250000, 0.992500]
    cap1s_upper = [1.014000, 10.075000, 100.750000, 1.007500]
    cap2s_lower = [9.925000, 109.200000, 0.992500, 9.875000]
    cap2s_upper = [10.075000, 110.800000, 1.007500, 10.125000]
    for i in range(4):
        status = 'pass'
        if cap1s_lower[i] > float(cap1[i]) or cap1s_upper[i] < float(cap1[i]):
            status = 'fail'
            print(Colors.FAIL +
                  f'{cap1_desc[i]}    {cap1[i]}    {cap1s_lower[i]}    {cap1s_upper[i]}    {status}'
                  + Colors.RESET)
            os.system('pause')
        else:
            print(f'{cap1_desc[i]}    {cap1[i]}    {cap1s_lower[i]}    {cap1s_upper[i]}    {status}')
    for i in range(4):
        status = 'pass'
        if cap2s_lower[i] > float(cap2[i]) or cap2s_upper[i] < float(cap2[i]):
            status = 'fail'
            print(Colors.FAIL +
                  f'{cap2_desc[i]}    {cap2[i]}    {cap2s_lower[i]}    {cap2s_upper[i]}    {status}'
                  + Colors.RESET)
            os.system('pause')
        else:
            print(f'{cap2_desc[i]}    {cap2[i]}    {cap2s_lower[i]}    {cap2s_upper[i]}    {status}')


if __name__ == '__main__':
    a = ConnectedUUT()
    a.ins.write('*CLS;*RST')
    reset()
    idn = a.ins.query('*IDN?')
    print(idn)
    stat_ok = a.ins.query('CAL:PROT:STAT?')
    isr_ok = '6145\n'

    print('連結 5520 normal 與 3510 input(要拔除3510 TC input.')
    os.system('pause')
    os.system('cls')

    cal_tco()

    vef_tco()

    os.system('pause')
