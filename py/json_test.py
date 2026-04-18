import json

data = {
    "balance": 450.0,
    "transactions": [
      {"type": "deposit", "amount": 300.0, "balance": 750.0},
      {"type": "withdrawal", "amount": 50.0, "balance": 450.0}
    ]
}
data["transactions"].append({"type": "deposit", "amount": 300.0, "balance": 750.0})

with open("bank_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open("bank_data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print(loaded_data)
print(type(loaded_data))
print(type(loaded_data["balance"]))
print(type(loaded_data["transactions"]))
print(type(loaded_data["transactions"][0]))
print(type(loaded_data["transactions"][0]["type"]))
print(type(loaded_data["transactions"][0]["amount"]))