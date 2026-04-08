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

def get_choice():
    print("===Welcome to Mini Bank===")
    print("Enter '1' to deposit")
    print("Enter '2' to withdraw")
    print("Enter '3' to check balance")
    print("Enter '4' to view transaction history")
    print("Enter '5' to view summary")
    print("Enter '0' to exit")
    choice = input("Enter your choice here: ").strip()
    return choice

def login(user_worker):
    while True:
        user_id = input("Enter your ID: ").strip()
        try:
            user_id = int(user_id)
            if user_id <= 0:
                print("ID must be greater than 0.")
                continue
        except ValueError:
            print("Please enter a number.")
            continue
        user = user_worker.get_user(user_id)
        if user is None:
            print("User not found.")
            continue
        return user_id