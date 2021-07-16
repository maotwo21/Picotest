from UUTCommand import ConnectedUUT
from UUTCommand import verification_zero
from UUTCommand import text_save

# 必要宣告
a = ConnectedUUT()
a.uut.query('*IDN?')

# uut DC 0.1V
a.uut.write('CONF:VOLT:DC 0.1')
a.uut.write('VOLT:NPLC 10')
# 電供 0V
a.supply.write('volt 0')
a.supply.write('outp 1')
# 零點驗證
point = verification_zero()
# 將值存入資料檔，量測點為point_name
point_name = 'DC100mV_0V = ' + str(point)
text_save(a.idn, point_name)

"""
# uut AC 0.1V
a.uut.write('CONF:VOLT:AC 0.1')
a.uut.write('DET:BAND 3')
a.supply.write('volt 0')
a.supply.write('outp 1')
point = verification_zero()
point_name = 'AC100mV_0V = ' + str(point)
text_save(a.idn, point_name)

# uut AC 1V
a.uut.write('SENSE:VOLT:AC:RANGE 1')
point = verification_zero()
point_name = 'AC1V_0V = ' + str(point)
text_save(a.idn, point_name)






"""
