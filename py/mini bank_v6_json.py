import json

def save_data(data, filename="bank_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(filename="bank_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            return loaded_data
    except FileNotFoundError:
        return {"balance": 0.0, "transactions": []}
    except json.JSONDecodeError:
        return {"balance": 0.0, "transactions": []}

def get_valid_amount(prompt):
    while True:
      amount_raw = input(prompt).strip()
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

def get_note():
    while True:
        note = input("Enter note (Max len 10) or Leave it blank: ").strip()
        if len(note) > 10:
            print("Note is too long.")
            continue
        return note

def handle_deposit():
    data = load_data()
    amount = get_valid_amount("Please enter your deposit amount, or press 'Q' to go back: ")
    if amount is None:
        print(f"Your balance: {data['balance']:.2f}")
        return

    note = get_note()
    data["balance"] += amount
    data["transactions"].append({
        "type": "deposit",
        "amount": amount,
        "balance": data["balance"],
        "note": note
        })
    save_data(data)
    print(f"Deposit successful. Current balance: {data['balance']:.2f}")
    return

def handle_withdrawal():
    data = load_data()
    if data["balance"] <= 0:
        print(f"Insufficient balance. You cannot withdraw: {data['balance']:.2f}")
        return

    while True:
        amount = get_valid_amount("Please enter withdrawal amount, or press 'Q' to go back: ")
        if amount is None:
            return

        if amount > data["balance"]:
            print(f"Insufficient balance. Current balance: {data['balance']:.2f}")
            continue

        note = get_note()
        data["balance"] -= amount
        data["transactions"].append({
        "type": "withdrawal",
            "amount": amount,
            "balance": data["balance"],
            "note": note
        })
        save_data(data)
        print(f"Withdrawal successful. Current balance: {data['balance']:.2f}")
        return

def show_transactions():
    data = load_data()
    transactions = data["transactions"]
    if not transactions:
        print("No transactions yet.")
        return

    for i, tx in enumerate(transactions, start=1):
        note = tx.get('note') or 'No note'
        print(f"{i}. Type: {tx['type'].title()}, Amount: {tx['amount']:.2f}, Balance: {tx.get('balance', 0.0):.2f}, Note: {note}")

def show_summary():
    data = load_data()
    transactions = data["transactions"]
    if not transactions:
        print("No transactions yet.")
        return

    deposit_count = 0
    deposit_total = 0.0
    withdrawal_count = 0
    withdrawal_total = 0.0

    for tx in transactions:
        if tx["type"] == "deposit":
            deposit_count += 1
            deposit_total += tx["amount"]
        elif tx["type"] == "withdrawal":
            withdrawal_count += 1
            withdrawal_total += tx["amount"]
    current_balance = data["balance"]
    print("=")
    print(f"Deposit Count: 【{deposit_count}】")
    print(f"Deposit Total: 【{deposit_total:.2f}】")
    print(f"Withdrawal Count: 【{withdrawal_count}】")
    print(f"Withdrawal Total: 【{withdrawal_total:.2f}】")
    print(f"Current Balance: 【{current_balance:.2f}】")
    print("=")
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
        handle_deposit()

    elif choice == "2":
        handle_withdrawal()

    elif choice == "3":
        data = load_data()
        print(f"Your current balance: {data['balance']:.2f}")

    elif choice == "4":
        show_transactions()

    elif choice == "5":
        show_summary()

    elif choice == "0":
        print("Thank you for using Mini Bank.")
        break

    else:
        print("Please enter a number 1/2/3/4/5/0.")
        continue