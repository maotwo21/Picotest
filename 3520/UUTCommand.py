import pyvisa
import time


# 抓取有用到的USB port
class ConnectedUUT:
    def __init__(self):
        rm = pyvisa.ResourceManager()  # 從pyvisa抓取
        uut_tuples = rm.list_resources()  # 資料類型是tuples
        uut_list = list(uut_tuples)  # 把資料類型改成list
        # 從uut_list拿掉沒有用到的port跟電供port
        for i in range(0, 3):
            uut_list.pop()
        uut_list.remove('USB0::0x164E::0x258A::TW00036148::INSTR')
        # 啟用電供
        self.supply = rm.open_resource('USB0::0x164E::0x258A::TW00036148::INSTR')  # 電供的USB_port
        # 啟用第X台uut
        idn = str(rm.open_resource(uut_list[0]))
        self.idn = idn[39:49]
        self.uut = rm.open_resource(uut_list[0])


# 從TXT找各個驗證點的公差
class Tolerance:
    def __init__(self, word):
        filename = "D:/Users/User/PycharmProjects/pythonProject/3520/VEF range_351X.txt"  # 檔案位置
        try:
            with open(filename, 'r') as file:
                for i in file:
                    tol = file.readline()  # 每行個別查找
                    if str(word) in tol:
                        tol1 = tol.find(str('='))  # 以TXT檔紀錄的格式分別出read 跟range 的公差
                        tol2 = tol.find(str('+'))
                        reading = tol[tol1 + 2:tol2]
                        limit = tol[tol2 + 1:-1]  # python裡的range有用到，用limit代替
                        self.reading = reading  # 將屬性寫入物件裡
                        self.limit = limit
                        break
        # 檔案不存在的例外處理
        except FileNotFoundError:
            print("VEF range不存在。")
        # 路徑為目錄的例外處理
        except IsADirectoryError:
            print("該路徑為目錄")


# 驗證零點
def verification_zero():
    a = ConnectedUUT()
    # 零點的tolerance
    zero = Tolerance('ZERO')
    # 設定:電供值、uut允許的上下限
    supply1 = float(a.supply.query('VOLTage?'))
    lower_limit = supply1 - (int(zero.limit) * 0.000001)
    upper_limit = supply1 + (int(zero.limit) * 0.000001)
    # 執行時間為6秒
    t_end = time.time() + 6
    while time.time() < t_end:
        uut1 = float(a.uut.query('read?'))
        uut1 = round(uut1, 6)
        uut2 = float(a.uut.query('read?'))
        uut2 = round(uut2, 6)
        if ((uut1 > lower_limit) & (uut1 < upper_limit)) & ((uut2 > lower_limit) & (uut2 < upper_limit)):
            err = a.uut.query('SYST:ERR?')  # 讀完error後，機子的error會消失
            if 'no error' not in err:
                return uut2  # 將範圍內的值放入txt
            else:
                a.supply.write('outp 0')  # 有error的話先關電源
                print(err)
                exit()
    return uut2  # 將範圍外的值放入txt


def text_save(filename, data):
    with open(filename, 'a') as file:
        file.write(data)
        file.write('\n')
