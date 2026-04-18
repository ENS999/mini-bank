while True:
    print("=== Notes 選單 ===")
    print("1. 新增筆記")
    print("2. 查看全部筆記")
    print("3. 離開筆記")
    choice = input("請輸入選項: ")

    if choice == "1":
        notes = input("請輸入內容: ")
        with open("notes.txt", "a", encoding="utf-8") as f:
            f.write(notes + "\n")
    elif choice == "2":
        try:
            with open("notes.txt", "r", encoding="utf-8") as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print("請新增一行筆記。")
    elif choice == "3":
        print("感謝您使用筆記本。")
        break
    else:
        print("請輸入選項數字。")