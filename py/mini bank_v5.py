TX_FILE = "transactions.txt"
def load_transactions(filename=TX_FILE):
    txs = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue
                tx_type = parts[0].strip().lower()
                try:
                    amount = float(parts[1])
                    balance = float(parts[2])
                except ValueError:
                    continue
                tx = (tx_type, amount, balance)
                txs.append(tx)
    except FileNotFoundError:
        return []
    return txs

def load_balance():
    txs = load_transactions()
    if not txs:
        return 0.0
    return txs[-1][2]

balance = load_balance()

def log_transactions(tx_type, amount, balance):
    with open(TX_FILE, "a", encoding="utf-8") as f:
        f.write(f"{tx_type},{amount:.2f},{balance:.2f}\n")

def get_valid_amount(prompt):
    while True:
      amount_raw  = input(prompt).strip()
      if amount_raw.lower() == "q":
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

def handle_deposit(balance):
    amount = get_valid_amount("Please enter your deposit amount, or press 'Q' to go back: ")
    if amount is None:
        print(f"Your balance: {balance:.2f}")
        return balance

    balance += amount
    print(f"Deposit successful. Current balance: {balance:.2f}")
    log_transactions("deposit", amount, balance)
    return balance

def handle_withdrawal(balance):
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
        log_transactions("withdrawal", amount, balance)
        return balance

def show_transactions():
    txs = load_transactions()
    if not txs:
        print("No transactions yet.")
        return
    for tx_type, amount, balance in txs:
        print(f"{tx_type.title()}, {amount:.2f}, {balance:.2f}")

def show_summary():
    txs = load_transactions()
    if not txs:
        print("No transactions yet.")
        return

    deposit_count = 0
    deposit_total = 0.0
    withdrawal_count = 0
    withdrawal_total = 0.0

    for tx_type, amount, balance in txs:
        if tx_type == "deposit":
            deposit_count += 1
            deposit_total += amount
        elif tx_type == "withdrawal":
            withdrawal_count += 1
            withdrawal_total += amount
        corrent_balance = txs[-1][2]
    print(f"Deposit Count: {deposit_count}, Deposit Total: {deposit_total:.2f}")
    print(f"Withdrawal Count: {withdrawal_count}, Withdrawal Totla: {withdrawal_total:.2f}")
    print(f"Current Balance: {corrent_balance:.2f}")
    return

def get_choice():
    print("===Welcome to Mini Bank===")
    print("Enter '1' to deposit")
    print("Enter '2' to withdraw")
    print("Enter '3' to check balance")
    print("Enter '4' to view transaction history")
    print("Enter '5' to view summary")
    print("Enter '0' to exit")
    choice = input("Enter your choice here: ")
    return choice

while True:
    choice = get_choice()
    if choice == "1":
        balance = handle_deposit(balance)

    elif choice == "2":
        balance = handle_withdrawal(balance)

    elif choice == "3":
        print(f"Your current balance: {balance:.2f}")

    elif choice == "4":
        show_transactions()

    elif choice == "5":
        show_summary()

    elif choice == "0":
        print("Thank you for using Mini Bank.")
        break

    else:
        print("Please enter a number 1/2/3/4/0.")
        continue