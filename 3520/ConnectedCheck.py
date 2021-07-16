import time
from UUTCommand import Tolerance
from UUTCommand import ConnectedUUT


# 檢查UUT跟supply之間的連線
def connect_check():
    # 宣告uut跟supply
    connection = ConnectedUUT()  # a為這次程式執行的代號
    # uut、電供重製
    connection.uut.write('*CLS')
    connection.uut.write('*RST')
    connection.supply.write('*CLS')
    connection.supply.write('*RST')
    # met_cal用Ohm檔驗證
    """connection.uut.write('conf:fres 100')
    connection.uut.write('AVERAGE:STATE OFF')
    connection.uut.write('fres:nplc 10')"""
    # 電供 沒Ohm 先用1 v假設
    connection.uut.write('conf:volt 1')
    connection.uut.write('AVERAGE:STATE OFF')
    connection.uut.write('volt:nplc 10')
    # 電供 1V
    connection.supply.write('outp 1')
    connection.supply.write('VOLT 1')
    # 零點的tolerance
    zero = Tolerance('ZERO')
    # 設定:電供值、uut允許的上下限
    supply1 = float(connection.supply.query('VOLTage?'))
    lower_limit = supply1 - (100 * int(zero.limit) * 0.000001)
    upper_limit = supply1 + (100 * int(zero.limit) * 0.000001)
    # uut開空值功能，因為用電壓測試，空值功能先關閉
    """connection.uut.write('CALC:FUNC NULL')
    connection.uut.write('CALC:STATE ON')
    connection.uut.query('read?')"""
    # 執行時間為6秒
    t_end = time.time() + 6
    while time.time() < t_end:
        uut1 = float(connection.uut.query('read?'))
        uut1 = round(uut1)
        uut2 = float(connection.uut.query('read?'))
        uut2 = round(uut2)
        if ((uut1 > lower_limit) & (uut1 < upper_limit)) & ((uut2 > lower_limit) & (uut2 < upper_limit)):
            connection.uut.write('CALC:STATE off')
            print('傳輸線已連結')
            break
    # 若讀取值不在標準內print檢查連線
    connection.supply.write('outp 0')
    if ((uut1 < lower_limit) or (uut1 > upper_limit)) or ((uut2 < lower_limit) or (uut2 > upper_limit)):
        print('檢查P961XA是否連結UUT')
