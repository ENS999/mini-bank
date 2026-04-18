entry = float(input("Entry price: "))
stop  = float(input("Stop price: "))
exit_price = float(input("Exit price: "))

risk = entry - stop
profit = exit_price - entry

if risk == 0:
    print("Entry price and stop price are the same. Cannot compute R.")

else:
    r_multiple = profit / risk
    print(f"this trade is {r_multiple:.2f}R")
    print(f"risk: {risk}, profit: {profit}")
