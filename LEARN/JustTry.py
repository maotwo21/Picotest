S = input("輸入一個數字").strip()
try:     
    print(int(S))
except Exception as e:
    print(e)
else:
    print("Good String")
finally:
    print("Final")