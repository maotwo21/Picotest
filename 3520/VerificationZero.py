from UUTCommand import ConnectedUUT
from UUTCommand import verification_zero
from UUTCommand import text_save

a = ConnectedUUT()
a.uut.query('*IDN?')
# uut 0.1V range
a.uut.write('CONF:VOLT:DC 0.1')
a.uut.write('VOLT:NPLC 10')
# 電供 0V
a.supply.write('volt 0')
a.supply.write('outp 1')
# 零點驗證
point = verification_zero()
point_name = 'DC100mV_0V = '
point = (point_name + str(point))
# 創建驗證資料檔
with open(a.idn, 'w') as file:
    file.write(a.idn)
    file.write('\n')
# 將值存入資料檔
text_save(a.idn, point)
