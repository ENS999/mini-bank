while True:
    entry_raw = input("Entry pirce: ")
    try:
        entry = float(entry_raw)
    except ValueError:
        print("Please enter a number。 Do not enter text or symbols。")
        continue
    if entry <= 0:
        print("The price must be greater than 0。")
        continue
    break

while True:
    stop_raw = input ("Stop price: ")
    try:
        stop = float(stop_raw)
    except ValueError:
        print("Please enter a number。 Do not enter text or symbols。")
        continue
    if stop <= 0:
        print("The price must be greater than 0。")
        continue
    break

while True:
    exit_raw = input("Exit price: ")
    try:
        exit_price = float(exit_raw)
    except ValueError:
        print("Please enter a number。 Do not enter text or symbols。")
        continue
    if exit_price <= 0:
        print("The price must be greater than 0。")
        continue
    break

risk = entry - stop
profit = exit_price - entry

if risk == 0:
    print("Since the entry_price and stop_price are the same, it's impossible to calculate R")

else:
    r_multiple = profit / risk
    print(f"risk: {risk}, profit: {profit}")
    print(f"This trade is: {r_multiple:.2f}R")