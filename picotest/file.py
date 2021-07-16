import os.path
import time
from datetime import datetime
import shutil
import sys
# 檢查有沒有路徑參數
if len(sys.argv) < 2:
    print("將資料夾拉到.exe上")
    os.system("pause")
    exit()
# 資料夾的路徑
filepath = sys.argv[1]
# 得到資料夾路徑下的所有文件名稱
files = os.listdir(filepath)
for file in files:  # 搜尋整個文件夾(依照資料夾內的檔案數目決定執行次數)
    if not os.path.isdir(file):  # 檢查是不是目錄(資料夾)
        FileExt = os.path.splitext(file)  # 不是目錄的話把檔名跟副檔名分開
        if FileExt[1] != "" and FileExt[1] != ".lnk":  # 副檔名不是空白也不是連結檔
            OldPath = filepath+"/"+file  # 資料夾路徑+檔案(檔案路徑)
            FileDate = time.ctime(os.stat(OldPath).st_mtime)  # 檔案最后一次修改的时间
            FileMDate = FileDate.split()  # 把時間分開(以空格分割時間,EX:Thu Jun 10 10:12:35 2021)
            name = datetime.strptime(FileMDate[-1]+"-"+FileMDate[1]+"-"+FileMDate[2], "%Y-%b-%d")  # 將字串轉換回數字
            NewPath = filepath+"/"+name.strftime('%Y%m%d')  # 新路徑為資料夾路徑+檔案修改日期
            if os.path.isdir(NewPath):  # 檢查新路徑是不是目錄(資料夾)
                shutil.move(OldPath, NewPath)  # 是的話移動檔案到下層時間目錄
                print(OldPath+" to "+NewPath)
            else:
                os.mkdir(NewPath)  # 不是的話創建目錄
                shutil.move(OldPath, NewPath)  # 移動檔案到下層時間目錄
                print(OldPath+" to "+NewPath)
