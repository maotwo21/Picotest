import pyvisa

# 抓取有用到的USB port
rm = pyvisa.ResourceManager()  # 從pyvisa抓取
uut_tuples = rm.list_resources()  # 資料類型是tuples
uut_list = list(uut_tuples)  # 把資料類型改成list
# 啟用第X台uut
uut = rm.open_resource(uut_list[0])
print(uut_list)
idn = str(rm.open_resource(uut_list[0]))
idn = idn[39:-10]
# 檢查儀器是否連結
if 'idn' not in locals():
    print('沒有USB儀器')
    input()
    exit()
# 儀器序號
print('\n\n\n       目前連結的儀器為' + idn)
date = input('\n       請輸入校正日期\n')
# 判斷UUT是 2110 OR 3510
if len(idn) < 9:
    uut.write('cal:prot:code p8125652;init')
    uut.write('cal:coun:back:zero')

# 寫入校正日期
uut.write('cal:prot:date ' + '"' + date + '"')
uut.write("cal:prot:lock")
