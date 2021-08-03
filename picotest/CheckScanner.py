import pyvisa

rm = pyvisa.ResourceManager()  # 從 pyvisa 訪問 ni-visa
ins_tuples = rm.list_resources()  # 資料類型是 tuples
usb_ins = [i for i in ins_tuples if 'USB' in i]  # 把資料類型改成list，只拿用USB連接的儀器

if usb_ins:
    usb = rm.open_resource(usb_ins[0])
else:
    usb = 0
    input('沒有檢測到USB')
    exit()

for i in range(20):
    usb.write(f'ROUTe:SCAN:FUNCtion {i+1},"VOLT:DC"')
usb.write('ROUTe:SCAN:SCAN')

for i in range(10):
    a = usb.query(f'ROUTe:SCAN:FUNC? {i+1}')
    if a == '"NONE"\n':
        input(f'CHANNEL {i+1}測試失敗')
input('測試結束')
