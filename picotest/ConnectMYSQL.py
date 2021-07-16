import mysql.connector
import sys
import os
import time


# 上傳系統驗證點
def upload1(self):
    with open(self, "r", encoding='utf-8') as f:
        lines = f.readlines()
        row_num = 0
        # 找時間
        for i in lines:
            # 檢查需要上傳的字串
            if i.find("Date") != -1:  # find()的回傳值不是-1(有pass那行)
                dates = i.split()
                date = dates[1]
                print(date)
                break
        #  找SN
        for i in lines:
            if i.find("Serial Number") != -1:  # find()的回傳值不是-1(有pass那行)
                sns = i.split()
                sn1 = sns[2]
                dot = sn1.find('.')
                sn = sn1[1:dot]
                print(sn)
                break
        # 建立每一項測試的上傳資料
        for i in lines:
            if i.find('@') != -1:
                if i.find('OHMS') != -1:
                    row_num += 1  # 測試編號
                    tests = i.split("'")
                    test_desc = tests[0]
                    fix = tests[-4]
                    var = tests[-3]
                    lower = tests[-2]
                    uppers = tests[-1].split()
                    upper = uppers[0]
                    status = uppers[2]
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()

                elif i.find('10KHz_1V') != -1:
                    row_num += 1  # 測試編號
                    tests = i.split("'")
                    test_desc = tests[0]
                    fix = test_desc.split()
                    fix = fix[0]
                    fix = int(fix)
                    fix = "{:.6f}".format(fix)
                    var = tests[-3]
                    lower = tests[-2]
                    uppers = tests[-1].split()
                    upper = uppers[0]
                    status = uppers[2]
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                        '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()
                else:
                    row_num += 1  # 測試編號
                    tests = i.split("'")
                    test_desc = tests[1]
                    fix = test_desc.split()
                    fix = fix[0]
                    var = tests[-3]
                    lower = tests[-2]
                    uppers = tests[-1].split()
                    upper = uppers[0]
                    status = uppers[2]
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()
    uut = f"""INSERT INTO UUT VALUES('{certificateNO}','{sn}','{date}') """
    cursor.execute(uut)
    connection.commit()


# 上傳ZERO驗證點
def upload2(self):
    with open(self+'.txt', "r", encoding='utf-8') as f:
        lines = f.readlines()
        row_num = 127
        # 測試名稱
        t_coup_desc = ['0 degC @ TCOUPL_TYPE_K', '50 degC @ TCOUPL_TYPE_K', '500 degC @ TCOUPL_TYPE_K',
                       '1000 degC @ TCOUPL_TYPE_K', '1372 degC @ TCOUPL_TYPE_K', '-200 degC @ TCOUPL_TYPE_K']
        cap1_desc = [' 1 nF @ CAP 1nf', ' 10 nF @ CAP 1nf', ' 100 nF @ CAP 1nf']
        cap2_desc = [' 1 uF @ CAP 1uf', ' 10 uF @ CAP 10uf', ' 110 uF @ CAP 100uf']
        cap3_desc = [' 1 mF @ CAP_1mf', ' 10 mF @ CAP_10mf']
        # 設定公差
        cap1s_lower = [0.986000, 0.986000, 99.250000]
        cap1s_upper = [1.014000, 10.075000, 100.750000]
        cap2s_lower = [0.992500, 9.925000, 109.200000]
        cap2s_upper = [1.007500, 10.075000, 110.800000]
        cap3s_lower = [0.992500, 9.875000]
        cap3s_upper = [1.007500, 10.125000]
        deg_lower = [-0.500000, 49.500000, 499.500000, 999.500000, 1371.500000, -200.500000]
        deg_upper = [0.500000, 50.500000, 500.500000, 1000.500000, 1372.500000, -199.500000]
        # 找電容，溫度的檔案資料，依照倍數分成3類
        for i in lines:
            # 需要上傳的字串列
            if i.find("CAP_1") != -1:
                cap11s = i.split('=')  # 拆出字串中需要的部分
                cap11s = cap11s[1].split(',')
            elif i.find("CAP_2") != -1:
                cap22s = i.split('=')
                cap22s = cap22s[1].split(',')
            elif i.find("TCOUP") != -1:
                t_coup = i.split('=')
                t_coup = t_coup[1].split(',')
        cap1s = [cap11s[0], cap11s[1], cap11s[2]]
        cap2s = [cap11s[3], cap22s[0], cap22s[1]]
        cap3s = [cap22s[2], cap22s[3]]
        if 'cap11s' in locals():
            print('有電容')
            for i in range(len(cap1s_lower)):  # list 元素數目
                if cap1s_lower[i] > (float(cap1s[i]) * 1E9) or cap1s_upper[i] < (float(cap1s[i]) * 1E9):
                    print(f'電容1超出範圍{cap1s[i]}')
                else:
                    row_num += 1  # 測試編號
                    test_desc = cap1_desc[i]
                    fix = test_desc.split()
                    fix = fix[0]
                    fix = int(fix)
                    fix = "{:.6f}".format(fix)
                    var = float(cap1s[i]) * 1E9
                    var = "{:.6f}".format(var)
                    lower = cap1s_lower[i]
                    lower = "{:.6f}".format(lower)
                    upper = cap1s_upper[i]
                    upper = "{:.6f}".format(upper)
                    status = 'pass'
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                        '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()
            for i in range(len(cap2s_lower)):
                if cap2s_lower[i] > (float(cap2s[i]) * 1E6) or cap2s_upper[i] < (float(cap2s[i]) * 1E6):
                    print(f'電容2超出範圍{cap2s[i]}')
                else:
                    row_num += 1  # 測試編號
                    test_desc = cap2_desc[i]
                    fix = test_desc.split()
                    fix = fix[0]
                    fix = int(fix)
                    fix = "{:.6f}".format(fix)
                    var = float(cap2s[i]) * 1E6
                    var = "{:.6f}".format(var)
                    lower = cap2s_lower[i]
                    lower = "{:.6f}".format(lower)
                    upper = cap2s_upper[i]
                    upper = "{:.6f}".format(upper)
                    status = 'pass'
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                        '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()
            for i in range(len(cap3s_lower)):
                if cap3s_lower[i] > (float(cap3s[i]) * 1E3) or cap3s_upper[i] < (float(cap3s[i]) * 1E3):
                    print(f'電容3超出範圍{cap3s[i]}')
                else:
                    row_num += 1  # 測試編號
                    test_desc = cap3_desc[i]
                    fix = test_desc.split()
                    fix = fix[0]
                    fix = int(fix)
                    fix = "{:.6f}".format(fix)
                    var = float(cap3s[i]) * 1E3
                    var = "{:.6f}".format(var)
                    lower = cap3s_lower[i]
                    lower = "{:.6f}".format(lower)
                    upper = cap3s_upper[i]
                    upper = "{:.6f}".format(upper)
                    status = 'pass'
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                        '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()
        if 't_coup' in locals():
            print('有溫度')
            for i in range(len(deg_lower)):
                if deg_lower[i] > float(t_coup[i]) or deg_upper[i] < float(t_coup[i]):
                    print(f'熱電偶超出範圍{t_coup[i]}')
                    os.system("pause")
                else:
                    row_num += 1  # 測試編號
                    test_desc = t_coup_desc[i]
                    fix = test_desc.split()
                    fix = fix[0]
                    fix = int(fix)
                    fix = "{:.6f}".format(fix)
                    var = float(t_coup[i])
                    var = "{:.6f}".format(var)
                    lower = deg_lower[i]
                    lower = "{:.6f}".format(lower)
                    upper = deg_upper[i]
                    upper = "{:.6f}".format(upper)
                    status = 'pass'
                    point = f"""INSERT INTO Calibration VALUES('{certificateNO}',
                                        '{row_num}','{test_desc}','{fix}','{var}','{lower}','{upper}','{status}') """
                    cursor.execute(point)
                    connection.commit()


if __name__ == "__main__":
    # 與資料庫建立連線
    connection = mysql.connector.connect(host='picotest815',
                                         database='coc',
                                         user='liao',
                                         password='Uo46qe07')
    cursor = connection.cursor()
    # 清理資料庫之前的資料
    cursor.execute('DELETE FROM UUT')
    cursor.execute('DELETE FROM Calibration')
    connection.commit()
    # 取檔案(第一份是.py軟體本身，第二份是testReport)
    args = sys.argv
    # 流水號
    with open('Certificate.txt', 'r') as file:  # 開啟流水號記事本
        certificateNO = file.readline()  # 只有一行流水號(7位數)
        print(certificateNO)
    new = int(certificateNO) + 1
    new = str(new)
    new = new.zfill(7)  # 流水號要7位數
    with open('Certificate.txt', 'w') as file:
        file.write(new)  # 寫入新流水號
    # 對testReport處理、上傳
    upload1(args[1])
    # 找電容溫度的檔案名稱
    arg = args[1].split("\\")
    arg = arg[-1].split("\\")
    arg = arg[-1].split("_")
    # 檢查檔案位置(依照.bat檔)
    txt = f'I:\\{arg[0]}.txt'
    print(txt)
    if os.path.isfile(txt):
        os.system(f'copy I:\\{arg[0]}.txt D:\\AutoReport')  # 複製到當前資料夾
    else:
        os.system(f'copy J:\\{arg[0]}.txt D:\\AutoReport')
    # 檢查檔案建立時間
    a = os.path.getmtime(f'{arg[0]}.txt')
    b = time.time()
    if b - a > 60 * 60 * 60 * 24 * 30:
        print('ZERO時間超過30天')
        exit()
    else:
        upload2(arg[0])
    cursor.close()
    os.system("pause")
