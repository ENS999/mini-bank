import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "notes.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("第一行 : Hello file!\n")
    f.write("第二行 : 這是測試文件檔\n")

print("寫入完成, 請去【這支 .py 檔所在的資料夾】看 notes.txt。")