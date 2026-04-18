while True:
    entry_raw = input("請輸入進場價: ")
    try:
        entry = float(entry_raw)
    except ValueError:
        print("請輸入數字，不要輸入文字或符號。")
        continue
    if entry <= 0:
        print("價格必須大於 0。")
        continue
    break

while True:
    stop_raw = input("請輸入停損價: ")
    try:
        stop = float(stop_raw)
    except ValueError:
        print("請輸入數字，不要輸入文字或符號")
        continue
    if stop <= 0:
        print("價格必須大於0。")
        continue
    break

while True:
    exit_raw = input("請輸入出場價: ")
    try:
        exit_price = float(exit_raw)
    except ValueError:
        print("請輸入數字，不要輸入文字或符號。")
        continue
    if exit_price <= 0:
        print("價格必須大於0。")
        continue
    break

risk = entry - stop
profit = exit_price - entry

if risk == 0:
    print("進場價與停損價一樣 沒辦法算R。")
else:
    r_multiple = profit / risk
    print(f"風險: {risk}, 獲利: {profit}")
    print(f"這一筆是 {r_multiple:.2f}R")

