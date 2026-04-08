from models import BankManager, UserWorker, AccountWorker, TransactionWorker
from services import handle_deposit, handle_withdrawal, register, get_summary, show_transactions
from utils import get_valid_amount, get_choice, login

manager = BankManager("bank.db")
manager.create_table()
cursor = manager.get_cursor()

user_worker = UserWorker(cursor)
account_worker = AccountWorker(cursor)
transaction_worker = TransactionWorker(cursor)


try:
    print("1：Login")
    print("2：Register")
    action = input("Enter your choice: ").strip()
    if action == "2":
        register(manager, user_worker, account_worker)  
    user_id = login(user_worker)
    account_id = account_worker.get_account_id_by_user(user_id)

    while True:
        choice = get_choice()
        if choice == "1":
            handle_deposit(manager, account_worker, transaction_worker, account_id)

        elif choice == "2":
            handle_withdrawal(manager, account_worker, transaction_worker, account_id)

        elif choice == "3":
            balance = account_worker.get_balance(account_id)
            print(f"Your current balance: {balance:.2f}")

        elif choice == "4":
            show_transactions(transaction_worker, account_id)

        elif choice == "5":
            get_summary(account_worker, transaction_worker, account_id)

        elif choice == "0":
            print("Thank you for using Mini Bank.")
            break

        else:
            print("Please enter a number 1/2/3/4/5/0.")
            continue
finally:
    manager.close()