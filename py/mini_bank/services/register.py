def register(manager, user_worker, account_worker):
    name = input("Enter your name: ").strip()
    try:
        user_id = user_worker.create_user(name)
        account_worker.create_user_account(user_id, "savings")
        manager.connection.commit()
        print(f"Register successful. Your user ID is {user_id}.")
        return
    except Exception:
        manager.connection.rollback()
        print("Registration failed.")
        return