import pyvisa
import os
import time
# 用pyvisa 連結儀器
rm = pyvisa.ResourceManager()
ins_list = rm.list_resources()
# 有usb字號的port
usb_ins = [i for i in ins_list if 'USB' in i]
# 確定只有一台UUT
if len(usb_ins) == 1:
    # 連結UsbPort
    ins = rm.open_resource(usb_ins[0])
    # 設定執行號碼
    i = 1
    # 重新開啟read.csv洗掉上一次的紀錄
    with open('read.csv', 'w+') as f:
        pass
    # 重複丟*IDN?給meter(i為次數,use_time為丟取時間)
    try:
        while True:
            start_time = time.time()
            value = ins.query('*IDN?')
            end_time = time.time()
            use_time = end_time - start_time
            display = 'Count%d, Read=%s, time=%.3f' % (i, value, use_time)
            # 顯示出進度
            print(display)
            # 將資料寫入read.csv
            with open('read.csv', 'a+') as f:
                f.writelines(display+'\n')
            i += 1
    # 用鍵盤使其停止會在csv黨後面加USER STOP
    except KeyboardInterrupt:
        with open('read.csv', 'a+') as f:
            f.writelines('\nUSER STOP\n')
        os.system('pause')
    # 結束後關閉meter
    finally:
        ins.close()
# 如果不是一台meter
else:
    print('meter 的數量不是一台!(沒插usb OR 連結2台以上的meter')
    os.system('pause')
rm.close()
