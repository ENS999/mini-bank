進場價 = float(input("輸入進場價: "))
停損價 = float(input("輸入停損價: "))
出場價 = float(input("輸入出場價: "))

風險 = 進場價 - 停損價
利潤 = 出場價 - 進場價

if 風險 == 0:
    print("本筆交易為0R: ")
else:
    R倍數 = 利潤 / 風險
    print(f"本筆交易為 {R倍數:.2f}R")
    print(f"風險: {風險}, 利潤: {利潤}")
