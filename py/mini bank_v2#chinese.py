餘額 = 0.0

while True:
    print("Welcome Mini Bank")
    print("存款請輸入 1: ")
    print("取款請輸入 2: ")
    print("查詢餘額請輸入 3: ")
    print("離開程式請輸入 0: ")
    選項 = input("在此輸入 : ")

    if 選項 == "1":
        while True:
            存款_raw = input("請輸入存款金額，或者按'Q'返回選單 : ")
            返回 = 存款_raw.strip().lower()
            if 返回 == "q":
                break
            try:
                存款 = float(存款_raw)
            except ValueError:
                print("請輸入金額或者按'Q'離開")
                continue
            if 存款 <= 0:
                print("金額請大於 0 ")
                continue
            餘額 = 餘額 + 存款
            print(f"存款成功，目前餘額為 {餘額:.2f}")
            break

    elif 選項 == "2":
        if 餘額 <= 0:
            print("餘額不足，無法取款。")
            continue
        while True:
            取款_raw = input("請輸入取款金額，或者按'Q'返回選單 : ")
            返回 = 取款_raw.strip().lower()
            if 返回 == "q":
                break
            try:
                取款 = float(取款_raw)
            except ValueError:
                print("請輸入金額或者按'Q'離開")
                continue
            if 取款 <= 0:
                print("金額請大於 0 ")
                continue
            if 取款 > 餘額:
                print(f"餘額不足，目前餘額為 {餘額:.2f}")
                continue
            餘額 = 餘額 - 取款
            print(f"取款成功，目前餘額為 {餘額:.2f}")
            break

    elif 選項 == "3":
        print(f"目前您的餘額為: {餘額:.2f}")
        continue

    elif 選項 == "0":
        print("感謝您使用迷你銀行")
        break

    else:
        print("請輸入 1/2/3/0")
        continue