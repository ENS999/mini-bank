while True:
    apple_raw = input("Apple deposit: ")
    try:
        apple = float(apple_raw)
    except ValueError:
        print("Please enter a number. Do not enter text or symbols.")
        continue
    if apple <= 0:
        print("The amount greater than 0.")
        continue
    break


while True:
    banana_raw = input("Banana deposit: ")
    try:
        banana = float(banana_raw)
    except ValueError:
        print("Please enter a number. Do not enter text or symbols.")
        continue
    if banana <= 0:
        print("The amount greater than 0.")
        continue
    break

Apple_price = 50
Banana_price = 100
total = apple * Apple_price + banana * Banana_price
print(f"Amount: {total:.2f}")