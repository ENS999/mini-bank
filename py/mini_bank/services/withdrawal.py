def handle_withdrawal(manager, account_worker, transaction_worker, account_id):
    balance = account_worker.get_balance(account_id)
    if balance <= 0:
        print(f"Your balance: {balance:.2f}")
        return
    while True:
        amount = get_valid_amount("Enter your amount: ")
        if amount is None:
            return
        if amount > balance:
            print(f"Your balance: {balance:.2f}")
            continue

        try:
            account_worker.handle_withdraw(account_id, amount)
            transaction_worker.create_transactions(account_id, "Withdraw", amount, "Self")
            manager.connection.commit()

            balance = account_worker.get_balance(account_id)
            print(f"Withdrawal successful. Your balance: {balance:.2f}")
            return
        except Exception:
            manager.connection.rollback()
            print("Transaction failed.")
            return