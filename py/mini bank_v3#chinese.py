餘額 = 0.0
交易紀錄 = []

def 處理存款(餘額, 交易紀錄):
    while True:
        存款_raw = input("請輸入存款金額, 或者按'Q'返回: ")
        返回 = 存款_raw.strip().lower()
        if 返回 == "q":
            return 餘額
        try:
            存款 = float(存款_raw)
        except ValueError: 
            print("請輸入數字, 或者'Q'返回")
            continue
        if 存款 <= 0:
            print("存款金額請大於 0 :")
            continue
        餘額 += 存款
        print(f"存款成功, 目前的餘額為: {餘額:.2f}")
        交易紀錄.append(("存款", 存款, 餘額))
        return 餘額


def 處理取款(餘額, 交易紀錄):
    if 餘額 <= 0:
        print("餘額不足無法取款。")
        return 餘額
    while True:
        取款_raw = input("請輸入取款金額, 或輸入'Q'返回: ")
        返回 = 取款_raw.strip().lower()
        if 返回 == "q":
            return 餘額
        try:
            取款 = float(取款_raw)
        except ValueError:
            print("請輸入數字, 或者'Q'返回")
            continue
        if 取款 > 餘額:
            print(f"餘額不足。目前餘額為: {餘額:.2f}")
            continue
        elif 取款 <= 0:
            print("取款金額請大於 0 :")
            continue
        餘額 -= 取款
        print(f"取款成功, 目前的餘額為: {餘額:.2f}")
        交易紀錄.append(("取款", 取款, 餘額))
        return 餘額

def 顯示交易紀錄(交易紀錄):
    if not 交易紀錄:
        print("目前沒有交易紀錄。")
        return
    print("===交易紀錄如下===")
    for 紀錄 in 交易紀錄:
        類型, 金額, 當下餘額 = 紀錄
        print(f"{類型}: {金額:.2f}, 當下餘額為: {當下餘額:.2f}")
    print("===以上===")

def 取得選項():
    print("===歡迎使用迷你銀行===")
    print("存款請輸入 1 : ")
    print("取款請輸入 2 : ")
    print("查詢餘額請輸入 3 : ")
    print("查詢交易紀錄請輸入 4 : ")
    print("離開迷你銀行請輸入 0 : ")
    選項 = input("請在此輸入: ")
    return 選項

while True:
    選項 = 取得選項()
    if 選項 == "1":
        餘額 = 處理存款(餘額, 交易紀錄)

    elif 選項 == "2":
        餘額 = 處理取款(餘額, 交易紀錄)

    elif 選項 == "3":
        print(f"目前餘額為: {餘額:.2f}")

    elif 選項 == "4":
        顯示交易紀錄(交易紀錄)

    elif 選項 == "0":
        print("感謝您使用本程式。")
        break

    else:
      print("請輸入1/2/3/4/0")
      continue