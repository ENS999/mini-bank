balance = 0.0

while True:
    print("Welcome to mini bank: ")
    print("1. Deposit amount: ")
    print("2. Withdraw amount: ")
    print("3. search balance: ")
    print("0. Exit mini bank: ")
    choice = input("Please enter choice: ")

    if choice == "1":
        while True:
            deposit_raw = input("Please enter deposit amount: ")
            try:
                deposit = float(deposit_raw)
            except ValueError:
                print("Please enter a number. Do not enter text or symbols.")
                continue
            if deposit <= 0:
                print("The amount must greater than 0.")
                continue
            break
        balance = balance + deposit
        print(f"Deposit success. Current balance: {balance:.2f}")

    elif choice == "2":
        if balance <= 0:
            print("Balance is 0. You cannot withdraw.")
            continue
        
        while True:
            withdraw_raw = input("Please enter withdraw amount: ")
            try:
                withdraw = float(withdraw_raw)
            except ValueError:
                print("Please enter a number. Do not enter text or symbols.")
                continue
            if withdraw <= 0:
                print("The amount must greater than 0.")
                continue
            if withdraw > balance:
                print("Insufficient balance.")
                print(f"Balance: {balance:.2f}")
                continue
            break
        balance = balance - withdraw
        print(f"Withdraw success. Current balance: {balance:.2f}")

    elif choice == "3":
        print(f"Current balance: {balance:.2f}")

    elif choice == "0":
        print("Thank you use mini bank.")
        break
    
    else:
        print("Error choice, please enter again.")