import pyvisa
import os


class ConnectedUUT:  # 連接快捷
    def __init__(self):
        rm = pyvisa.ResourceManager()  # 從pyvisa抓取
        ins_tuples = rm.list_resources()  # 資料類型是tuples
        usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
        gpib_ins = [i for i in ins_tuples if 'GPIB' in i]
        # 確定只有一台使用USB的儀器(電供不算)後，建立連結與id捷徑
        if len(usb_ins) == 1:
            self.ins = rm.open_resource(usb_ins[0])
        else:
            print('"Meter" 的數量不是一台!(沒插usb OR 連結2台以上的meter)')
            input('按 Enter 繼續')
            exit()


def vef_cap():
    print('拔除 5520 normal(3510 input 需插著)')
    input('按 Enter 繼續')
    os.system('cls')
    # 1nF的NULL值
    a.ins.write('CONF:CAP 1e-9')
    a.ins.write('SAMP:COUN 20')
    a.ins.write('CALC:FUNC AVER')
    a.ins.write('CALC:STAT 1')
    a.ins.query('READ?')
    null_max = a.ins.query('CALC:AVER:MAX?')
    null_min = a.ins.query('CALC:AVER:MIN?')
    null_1nf = (float(null_max)+float(null_min))/2
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
        null.append((float(null_max)+float(null_min))/2)
        a.ins.write('SAMP:COUN 1')
        a.ins.write('CALC:STAT 0')


if __name__ == '__main__':
    a = ConnectedUUT()
    a.ins.write('*CLS;*RST')
    idn = a.ins.query('*IDN?')
    print(idn)
    stat_ok = a.ins.query('CAL:PROT:STAT?')
    isr_ok = '6145\n'

    print('連結 5520 normal 與 3510 input(要拔除3510 TC input.')
    input('按 Enter 繼續')
    os.system('cls')

    vef_cap()

    input('按 Enter 結束')