balance = 0.0
transactions = []

def get_valid_amount(prompt):
    while True:
      amount_raw  = input(prompt)
      back = amount_raw.strip().lower()
      if back == "q":
          return None
      try:
          amount = float(amount_raw)
      except ValueError:
          print("Please enter a number, or press 'Q' to go back.")
          continue
      if amount <= 0:
          print("Amount must be greater than 0.")
          continue
      return amount

def handle_deposit(balance, transactions):
    amount = get_valid_amount("Please enter your deposit amount, or press 'Q' to go back: ")
    if amount is None:
        print(f"Your balance: {balance:.2f}")
        return balance

    balance += amount
    print(f"Deposit successful. Current balance: {balance:.2f}")
    transactions.append(("Deposit", amount, balance))
    return balance

def handle_withdrawal(balance, transactions):
    if balance <= 0:
        print(f"Insufficient balance. You cannot withdraw: {balance:.2f}")
        return balance

    while True:
        amount = get_valid_amount("Please enter withdrawal amount, or press 'Q' to go back: ")
        if amount is None:
            return balance

        if amount > balance:
            print(f"Insufficient balance. Current balance: {balance:.2f}")
            continue

        balance -= amount
        print(f"Withdrawal successful. Current balance: {balance:.2f}")
        transactions.append(("Withdrawal", amount, balance))
        return balance

def show_transactions(transactions):
    if not transactions:
        print("There are no transactions yet.")
        return

    print("=== Transactions History ===")
    for record in transactions:
        tx_type, amount, balance_after = record
        print(f"{tx_type}: {amount:.2f}, balance after: {balance_after:.2f}")
    print("===End===")

def get_choice():
    print("===Welcome to Mini Bank===")
    print("Enter '1' to deposit")
    print("Enter '2' to withdraw")
    print("Enter '3' to check balance")
    print("Enter '4' to view transaction history")
    print("Enter '0' to exit")
    choice = input("Enter your choice here: ")
    return choice

while True:
    choice = get_choice()
    if choice == "1":
        balance = handle_deposit(balance, transactions)

    elif choice == "2":
        balance = handle_withdrawal(balance, transactions)

    elif choice == "3":
        print(f"Your current balance: {balance:.2f}")

    elif choice == "4":
        show_transactions(transactions)

    elif choice == "0":
        print("Thank you for using Mini Bank.")
        break

    else:
        print("Please enter a number 1/2/3/4/0.")
        continue