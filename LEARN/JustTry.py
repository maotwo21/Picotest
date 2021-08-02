import os
import time
import pyvisa


class ConnectedUUT:  # 連接快捷
    def __init__(self):
        rm = pyvisa.ResourceManager()  # 從pyvisa抓取
        ins_tuples = rm.list_resources()  # 資料類型是tuples
        usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器
        usb_gpib = [i for i in ins_tuples if 'GPIB' in i]
        usb_net = [i for i in ins_tuples if 'TCPIP' in i]

        # 確定只有一台使用USB的儀器(電供不算)後，建立連結與id捷徑
        if len(usb_ins) == 1:
            self.ins = rm.open_resource(usb_ins[0])
            self.gpib = rm.open_resource('GPIB0::10::INSTR')
            self.net = rm.open_resource('GPIB0::4::INSTR')
        else:
            print('\n\n     確定 usb 連接數量及 5520 是否連接')
            input('\n\n     按 Enter 離開')
            exit()


if __name__ == '__main__':
    a = time.localtime()
    test_folder_position = 'D:\\test_folder\\' + str(a.tm_year) + '\\' + \
                           str(a.tm_mon).zfill(2) + '\\' + str(a.tm_mday).zfill(2)

    if os.path.isdir(test_folder_position):
        pass
    else:
        os.system(f'md "{test_folder_position}"')
