import xlrd
import csv
import sys
import os


def xls_to_csv(self):  # 將XLS轉換成CSV
    sheet = xlrd.open_workbook(self, logfile=open(os.devnull, 'w'))  # 讀取excel檔，將stdout重新定位到/dev/null
    table = sheet.sheet_by_index(0)  # 通過sheet索引獲取sheet工作表的物件(sheet1)
    with open('temp.csv', 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):  # 算出行數()
            row_value = table.row_values(row_num)  # 獲得第row_num行的資料列表
            write.writerow(row_value)  # 將單行寫成csv格式
    sheet.release_resources()  # 釋放檔案


def check():
    fail_points = []
    with open("temp.csv", "r", encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            # 有pass字串的話檢查測試值
            if str.lower(i).find("pass") != -1:  # find()的回傳值不是-1(有pass那行)
                for j in str.lower(i).split(","):  # 用，分隔每個字串
                    if "pass" in j:  # 找到pass的時候
                        position = str.lower(i).split(",").index(j)  # 設定PassPoint的位置叫position
                # 位置的順序是測試值,上限,下限,pass(position)
                if float(i.split(",")[position-3]) > float(i.split(",")[position-1]) or\
                        float(i.split(",")[position-3]) < float(i.split(",")[position-2]):  # 測試值大於上限或小於下限
                    fail_points.append("--FailPoint-- "+i.strip(" "))  # 在fail_points串列加入FailPoint i(去掉首尾空格)
                else:
                    count = 1  # pass的話count+1
            # 有fail字串的話，在fail_points串列加入FailPoint i(去掉空格)
            elif str.lower(i).find("fail") != -1:
                fail_points.append("--FailPoint-- "+i.strip(" "))
    # 如果fail_points串列沒有值
    if len(fail_points) == 0 and count == 1:
        print(arg+" ----Pass!\n")
    # 如果fail_points串列沒有值，count也等於0(csv檔裡沒有pass跟fail)
    elif len(fail_points) == 0 and count == 0:
        print("*"*(len(arg)+10))
        print(arg+"")
        print("找不到驗證資料，可能是檔案錯誤。")
        print("*"*(len(arg)+10)+"\n")
    # 如果fail_points串列有值，顯示那一行(檢查時存在fail_points)
    else:
        print("*"*(len(arg)+10))
        print(arg+"\n")
        for i in fail_points:
            print(i, end="")
        print("*"*(len(arg)+10)+"\n")


if __name__ == "__main__":
    args = sys.argv[1:]  # 取除程式本身之外的參數(0是CheckFail.py)
    for arg in args:  # 找出有幾個excel檔
        if os.path.isfile(arg):  # excel檔是否存在
            xls_to_csv(arg)  # 依照excel檔資料寫csv檔(temp.csv)
            check()
            os.remove("temp.csv")  # 移除csv檔
    print("共檢查了" + str(len(args)) + "項\n")
    os.system("pause")
