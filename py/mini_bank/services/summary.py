def show_transactions(transaction_worker, account_id):
    result = transaction_worker.get_transactions(account_id)
    if not result:
        print("No transactions found.")
        return
    for data in result:
        print(f"Account ID: {data[1]}. Type: {data[2]}, Amount: {data[3]:.2f}, Target: {data[4]} {data[5]}")

def get_summary(account_worker, transaction_worker, account_id):
    txs = transaction_worker.get_transactions(account_id)
    if not txs:
        print("No transactions found.")
        return