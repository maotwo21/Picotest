import pyvisa
import os

# looking the USB instrument port
rm = pyvisa.ResourceManager()  # 從pyvisa抓取
UUT_tuples = rm.list_resources()  # 資料類型是tuples
UUT_list = list(UUT_tuples)  # 把資料類型改成list

# 從UUT_list拿掉沒有用到的port跟電供port
for i in range(0, 3):
    UUT_list.pop()
UUT_list.remove('USB0::0x164E::0x258A::TW00036148::INSTR')  # 電供port

# 啟用電供
supply = rm.open_resource('USB0::0x164E::0x258A::TW00036148::INSTR')  # 電供的USB_port

# 啟用UUT跟建立UUT資料
filepath = 'UUT data/UUT list.csv'  # 資料位置
x = 0  # 第X台UUT
with open(filepath, 'a') as file:  # 建立所有UUT_IDN的資料表
    if os.stat(filepath).st_size == 0:  # 如果沒開頭
        file.write('instrument IDN, instrument usb\n')  # 開頭名稱
    for i in UUT_list:  # UUT數量
        instrument_USB = rm.open_resource(UUT_list[x])  # 啟用第X台UUT
        instrument_IDN = instrument_USB.query('Cal:sec:ser?')  # 讀第X台UUT的序號
        IDN = instrument_IDN.replace('\n', '').replace('\r', '')  # 去除空行
        # 將序號寫入資料表
        file.write(IDN)
        file.write(' ')
        # 將序號對應的USB port寫入資料表
        file.write(UUT_list[x])
        file.write('\n')
        x += 1  # 下一台UUT
