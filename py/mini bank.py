balance = 0.0
print(f"Initial balance: {balance:.2f}")

while True:
    deposit_raw = input("Deposit amount: ")
    try:
        deposit = float(deposit_raw)
    except ValueError:
        print("Please enter a number. Do not enter text or symbols.")
        continue
    
    if deposit <= 0:
        print("The amount must be greater than 0.")
        continue
    
    balance = balance + deposit
    break

print(f"Balance after deposit: {balance:.2f}")

while True:
    withdraw_raw = input("Withdraw amount: ")
    try:
        withdraw = float(withdraw_raw)
    except ValueError:
        print("Please enter a number. Do not enter text or symbols.")
        continue

    if withdraw <= 0:
        print("The amount greater than 0.")
        continue

    if withdraw > balance:
        print("Withdraw amount cannot be greater than balance.")
        print(f"Current balance: {balance:.2f}")
        continue

    balance = balance - withdraw
    break

print(f"Final balance: {balance:.2f}")