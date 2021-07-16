import win32com.client
import sys
import os
# 檢查bat參數
if len(sys.argv) < 2:
    print('設定參數小於2(應有一個名稱一個路徑)')
    os.system("pause")
    exit()
# 第一個參數為捷徑名稱
ShortCutName = sys.argv[1]
# 第二個參數為網路目標
TargetPath = sys.argv[2]
# 用WScript.Shell建造捷徑
shell = win32com.client.Dispatch('WScript.Shell')
# 建立並返回 WshShortcut 物件，.lnk為捷徑副檔名
shortcut = shell.CreateShortCut(ShortCutName+".lnk")
# 捷徑的原始檔位置
shortcut.TargetPath = TargetPath
# shortcut.WorkingDirectory = TargetPath.split("\\")[2]
shortcut.Arguments = '1' 
shortcut.save()
print("建立捷徑："+ShortCutName+".lnk 連結到："+TargetPath)
