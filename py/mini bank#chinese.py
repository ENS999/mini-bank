餘額 = 0.0

while True:
    存款_raw = input("請輸入存款金額: ")
    try:
        存款 = float(存款_raw)
    except ValueError:
        print("請輸入數字，不要輸入文字及符號")
        continue
    if 存款 <= 0:
        print("輸入金額需大於0")
        continue
    break

餘額 = 餘額 + 存款

while True:
    取款_raw = input("請輸入取款金額: ")
    try:
        取款 = float(取款_raw)
    except ValueError:
        print("請輸入數字，不要輸入文字及符號")
        continue
    if 取款 <= 0:
        print("輸入金額需大於0")
        continue
    if 取款 > 餘額:
        print("帳戶餘額不足")
        print(f"帳戶餘額為: {餘額:.2f}")
        continue
    break

餘額 = 餘額 - 取款
print(f"今日存入: {存款:.2f}, 今日取出: {取款:.2f}, 餘額: {餘額:.2f}")
