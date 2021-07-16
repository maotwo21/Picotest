class Text:
    # 把變數存入TXT
    def text_save(self, filename):
        with open(filename, 'a') as file:
            file.write(str(self))
            file.write(str('\n'))

    # 從TXT拿出變數
    def text_read(self):
        # 使用 try 開啟
        try:
            with open(str(self), 'r') as file:  # 開啟 self檔 read模式
                content = file.readlines()  #
                for i in range(len(content)):
                    content[i] = content[i][:len(content[i]) - 1]
                return content
        # 檔案不存在的例外處理
        except FileNotFoundError:
            print(str(self)+"不存在。")
        # 路徑為目錄的例外處理
        except IsADirectoryError:
            print("該路徑為目錄")
        # Try to read a txt file and return a list.Return [] if there was a mistake.
