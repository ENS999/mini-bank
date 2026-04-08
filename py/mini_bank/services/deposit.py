def handle_deposit(manager, account_worker, transaction_worker, account_id):
    amount = get_valid_amount("Enter your amount: ")
    if amount is None:
        return None
    try:
        account_worker.handle_deposit(account_id, amount)
        transaction_worker.create_transactions(account_id, "Deposit", amount, "Self")
        manager.connection.commit()

        balance = account_worker.get_balance(account_id)
        print(f"Deposit successful. Your balance: {balance:.2f}")
    except Exception:
        manager.connection.rollback()
        print("Transaction failed.")