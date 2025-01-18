import os

filepath = "./app/accounts.py"

if not os.path.exists(filepath):
    with open(filepath, "w", encoding = "utf-8")as file:
        file.write("hostname = ''\nusername = ''\npassword = ''")