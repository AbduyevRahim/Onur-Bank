import os
import time
from datetime import date, datetime
import json

DB_FILE = "bank_data.json"

# JSON file creation and initialization with default data if it doesn't exist
if not os.path.exists(DB_FILE):
    general_data = {
        "atm_cash": 5000.00,
        "users": [
            {
                "user": "user01",
                "password": "Test@123",
                "balance": 2500.00,
                "status": "active",
                "account_number": 10010001,
                "failed_attempt": 0,
                "daily_deposits": 0.0,
                "daily_withdrawals": 0.0,
                "daily_transfers": 0,
                "last_reset_date": date.today().isoformat(),
                "transactions": []
            },
            {
                "user": "user02",
                "password": "Test@456",
                "balance": 1500.00,
                "status": "active",
                "account_number": 10010002,
                "failed_attempt": 0,
                "daily_deposits": 0.0,
                "daily_withdrawals": 0.0,
                "daily_transfers": 0,
                "last_reset_date": date.today().isoformat(),
                "transactions": []
            },
            {
                "user": "user03",
                "password": "Test@789",
                "balance": 3000.00,
                "status": "active",
                "account_number": 10010003,
                "failed_attempt": 0,
                "daily_deposits": 0.0,
                "daily_withdrawals": 0.0,
                "daily_transfers": 0,
                "last_reset_date": date.today().isoformat(),
                "transactions": []
            }
        ]
    }
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(general_data, file, indent=4)

# Datas are read from the JSON file
with open(DB_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

is_logged_in = False

print("Welcome to the ONURbank system")

current_user = None
while current_user is None:
    included_username = input("Include your name: ").strip()
    
    for u in data["users"]:
        if isinstance(u, dict) and u.get("user") == included_username:
            current_user = u
            break
            
    if current_user is None:
        print("Incorrect username")

# Login process with password verification and account status check
if current_user:
    # Check if a new day has started
    current_date_str = date.today().isoformat()
    if current_user["last_reset_date"] != current_date_str:
        current_user["daily_deposits"] = 0.0
        current_user["daily_withdrawals"] = 0.0
        current_user["daily_transfers"] = 0
        current_user["last_reset_date"] = current_date_str
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    if current_user["status"] == "blocked":
        print("Maximum login attempt exceeded")
        print("Your card has been blocked")
        print("Please contact the bank administrator")
    else:
        included_password = input("Include your password: ")

        if current_user["password"] == included_password:
            print(f"Login is successful! Welcome {included_username}")
            print(f"Current balance: {current_user['balance']} AZN")
            is_logged_in = True
            current_user["failed_attempt"] = 0
            
            with open(DB_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        else:
            current_user["failed_attempt"] += 1
            print(f"Incorrect password. Attempt {current_user['failed_attempt']}/6")
            
            if current_user["failed_attempt"] == 3:
                print("Too many failed login attempts")
                for second in range(60, -1, -1):
                    time.sleep(1)
                    print(f"Please wait 00:{second:02d}", end="\r")
                print("\nYou may try again")
            
            while current_user["failed_attempt"] < 6:
                included_password = input("Include your password: ")
                if current_user["password"] == included_password:
                    print(f"Login is successful! Welcome {included_username}")
                    print(f"Current balance: {current_user['balance']} AZN")
                    is_logged_in = True
                    current_user["failed_attempt"] = 0
                    break
                else:
                    current_user["failed_attempt"] += 1
                    print(f"Incorrect password. Attempt {current_user['failed_attempt']}/6")

                    if current_user["failed_attempt"] == 3:
                        print("Too many failed login attempts")
                        for second in range(60, -1, -1):
                            time.sleep(1)
                            print(f"Please wait 00:{second:02d}", end="\r")
                        print("\nYou may try again")

            if current_user["failed_attempt"] >= 6:
                current_user["status"] = "blocked"
                print("Maximum login attempt exceeded")
                print("Your card has been blocked")
                print("Please contact the bank administrator")
            
            with open(DB_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)