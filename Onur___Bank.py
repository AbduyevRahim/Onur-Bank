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

# Main menu loop
if is_logged_in:
    while True:
        current_date_str = date.today().isoformat()
        if current_user["last_reset_date"] != current_date_str:
            current_user["daily_deposits"] = 0.0
            current_user["daily_withdrawals"] = 0.0
            current_user["daily_transfers"] = 0
            current_user["last_reset_date"] = current_date_str
            
            with open(DB_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                        
        print("="*40)
        print("        Python Banking System")
        print("="*40)
        print(f"Welcome! {included_username}")
        
        print("1. View Account Information")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Transaction History")
        print("7. Daily Limits")
        print("8. Change Password")
        print("9. Logout")
        print("0. Exit")
        print("="*40)
        
        choice = input("Choose an option: ")

        # 1. View Account Information    
        if choice == "1":
            print("View Account Information is selected")
            print(f"\nAccount Holder: {current_user['user']}")
            print(f"Account Number: {current_user['account_number']}")
            print(f"Available Balance: {current_user['balance']:.2f} AZN")
            print(f"Account Status: {current_user['status']}")

        # 2. Check Balance
        elif choice == "2":
            print("Check Balance is selected")
            print(f"\nCurrent Balance: {current_user['balance']:.2f} AZN")

        # 3. Deposit Money
        elif choice == "3":
            print("Deposit Money is selected")
            try:
                deposit_cash = float(input("Include deposit cash: "))
            except ValueError:
                print("\nError: Invalid amount format")
                continue

            if deposit_cash <= 0 or not (deposit_cash * 100).is_integer():
                print("\nError: Invalid amount")
            else:
                if current_user["daily_deposits"] + deposit_cash > 2000:
                    print("\nDeposit declined: daily limit would be exceeded")
                    print("Account balance and ATM cash remain unchanged")
                else:
                    balance_before = current_user["balance"]
                    current_user["daily_deposits"] += deposit_cash
                    current_user["balance"] += deposit_cash
                    data["atm_cash"] += deposit_cash
                    balance_after = current_user["balance"]
                    
                    tx_id = f"TXN{len(current_user.get('transactions', [])) + 1:04d}"
                    tx_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if "transactions" not in current_user:
                        current_user["transactions"] = []
                        
                    current_user["transactions"].append({
                        "id": tx_id,
                        "date": tx_time,
                        "type": "Deposit",
                        "amount": deposit_cash,
                        "balance_before": balance_before,
                        "balance_after": balance_after
                    })
                    
                    with open(DB_FILE, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                        
                    print(f"\nDeposit today: {current_user['daily_deposits']:.2f} AZN")
                    print(f"Requested deposit: {deposit_cash:.2f} AZN")
                    print(f"Daily deposit maximum: 2000 AZN")
                    print(f"Remaining deposit allowance: {2000-current_user['daily_deposits']:.2f} AZN")

        # 4. Withdraw Money
        elif choice == "4":
            print("Withdraw Money is selected")
            try:
                withdraw_cash = float(input("Include withdraw cash: "))
            except ValueError:
                print("\nError: Invalid amount format")
                continue

            if withdraw_cash <= 0 or not (withdraw_cash * 100).is_integer():
                print("\nError: Invalid withdraw amount")
            elif withdraw_cash > current_user["balance"]:
                print("\nError: Insufficient balance")
            elif data["atm_cash"] < withdraw_cash:  
                print("\nError: Insufficient ATM cash")
            elif current_user["daily_withdrawals"] + withdraw_cash > 1000:
                print("\nError: Daily withdraw limit is 1000 AZN")
            else:
                earlier_withdrawn = current_user["daily_withdrawals"]
                remaining_free = 500.0 - earlier_withdrawn
                if remaining_free < 0:
                    remaining_free = 0.0
                
                if withdraw_cash > remaining_free:
                    exceed_part = withdraw_cash - remaining_free
                    withdrawal_fee = exceed_part * 0.02
                else:
                    exceed_part = 0.0
                    withdrawal_fee = 0.0
                
                total_deducted = withdrawal_fee + withdraw_cash
                
                if total_deducted > current_user["balance"]:
                    print("\nError: Insufficient balance (including fee)")
                else:
                    balance_before = current_user["balance"]
                    current_user["balance"] -= total_deducted
                    data["atm_cash"] -= withdraw_cash               
                    current_user["daily_withdrawals"] += withdraw_cash
                    balance_after = current_user["balance"]
                    
                    tx_id = f"TXN{len(current_user.get('transactions', [])) + 1:04d}"
                    tx_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if "transactions" not in current_user:
                        current_user["transactions"] = []
                        
                    current_user["transactions"].append({
                        "id": tx_id,
                        "date": tx_time,
                        "type": "Withdrawal",
                        "amount": withdraw_cash,
                        "fee": withdrawal_fee,
                        "balance_before": balance_before,
                        "balance_after": balance_after
                    })
                    
                    with open(DB_FILE, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                    
                    print(f"\nCash withdrawn earlier today: {earlier_withdrawn:.2f} AZN")
                    print(f"New withdrawal request:        {withdraw_cash:.2f} AZN")
                    print(f"Remaining fee-free allowance: {remaining_free:.2f} AZN")
                    print(f"Amount charged at 2%:         {exceed_part:.2f} AZN")
                    print(f"Withdrawal commission:        {withdrawal_fee:.2f} AZN")
                    print(f"Amount deducted from account: {total_deducted:.2f} AZN")
                    print(f"Cash paid out:                {withdraw_cash:.2f} AZN")