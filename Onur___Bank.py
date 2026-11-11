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
        # 5. Transfer Money
        elif choice == "5":
            print("Transfer Money is selected")
            if current_user["daily_transfers"] < 5:
                try:
                    recipient_acc = int(input("Include recipient account number: "))
                except ValueError:
                    print("\nError: Invalid account number format")
                    continue
                
                recipient_user = None
                for u in data["users"]:
                    if isinstance(u, dict) and u.get("account_number") == recipient_acc:
                        recipient_user = u
                        break
                        
                if recipient_user:
                    if recipient_user["user"] == current_user["user"]:
                        print("\nError: You cannot transfer money to your own account!")
                    else:
                        print(f"\nRecipient found: {recipient_user['user']}")
                        try:
                            transfer_cash = float(input("Include transfer cash: "))
                        except ValueError:
                            print("\nError: Invalid amount format")
                            continue

                        if transfer_cash <= 0 or current_user["balance"] < transfer_cash:
                            print("\nError: Invalid transfer amount or insufficient balance")     
                        else:       
                            confirmation = input("Confirm transfer (Y/N): ").upper()
                            if confirmation == "N":
                                print("\nTransfer cancelled.")
                            elif confirmation == "Y":
                                sender_balance_before = current_user["balance"]
                                current_user["daily_transfers"] += 1
                                current_user["balance"] -= transfer_cash
                                sender_balance_after = current_user["balance"]
                                
                                tx_id_sender = f"TXN{len(current_user.get('transactions', [])) + 1:04d}"
                                tx_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                if "transactions" not in current_user:
                                    current_user["transactions"] = []
                                    
                                current_user["transactions"].append({
                                    "id": tx_id_sender,
                                    "date": tx_time,
                                    "type": "Transfer Sent",
                                    "recipient_account": recipient_user["account_number"],
                                    "amount": -transfer_cash,
                                    "balance_before": sender_balance_before,
                                    "balance_after": sender_balance_after
                                })

                                recipient_balance_before = recipient_user["balance"]
                                recipient_user["balance"] += transfer_cash
                                recipient_balance_after = recipient_user["balance"]
                                
                                tx_id_rec = f"TXN{len(recipient_user.get('transactions', [])) + 1:04d}"
                                if "transactions" not in recipient_user:
                                    recipient_user["transactions"] = []
                                    
                                recipient_user["transactions"].append({
                                    "id": tx_id_rec,
                                    "date": tx_time,
                                    "type": "Transfer Received",
                                    "sender_account": current_user["account_number"],
                                    "amount": transfer_cash,
                                    "balance_before": recipient_balance_before,
                                    "balance_after": recipient_balance_after
                                })
                                
                                with open(DB_FILE, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                    
                                print(f"\nSender: {current_user['user']}")
                                print(f"Recipient account: {recipient_user['account_number']}")
                                print(f"Recipient: {recipient_user['user']}")
                                print(f"Amount: {transfer_cash:.2f} AZN")
                                print("\nTransfer successful!")
                                print(f"Sender new balance: {current_user['balance']:.2f} AZN")
                            else:
                                print("\nError: Invalid confirmation")
                else:
                    print("\nError: Invalid account number")
            else:
                print("\nError: Daily transfer limit exceeded (5 times)")

        # 6. Transaction History
        elif choice == "6":
            print("Transaction History is selected")
            print("\n=========== TRANSACTION HISTORY ===========")
            transactions = current_user.get("transactions", [])
            if not transactions:
                print("No transaction history available for this account.")
            else:
                for tx in transactions[-10:]:
                    print(f"ID: {tx['id']}")
                    print(f"Date: {tx['date']}")
                    print(f"Type: {tx['type']}")
                    if "recipient_account" in tx:
                        print(f"Recipient account: {tx['recipient_account']}")
                    if "sender_account" in tx:
                        print(f"Sender account: {tx['sender_account']}")
                    print(f"Amount: {tx['amount']:.2f} AZN")
                    if "fee" in tx and tx["fee"] > 0:
                        print(f"Withdrawal Commission: {tx['fee']:.2f} AZN")
                    print(f"Balance before: {tx['balance_before']:.2f} AZN")
                    print(f"Balance after: {tx['balance_after']:.2f} AZN")
                    print("-" * 35)
            print("===========================================")

        # 7. Daily Limits
        elif choice == "7":
            fee_remaining = 500.0 - current_user["daily_withdrawals"]
            if fee_remaining < 0:
                fee_remaining = 0.0
            print("=========== DAILY LIMITS ===========")
            print(f"Deposit used: {current_user['daily_deposits']:.2f} / 2000 AZN")
            print(f"Deposit remaining:    {2000-current_user['daily_deposits']:.2f} AZN")
            print(f"Cash withdrawn:    {current_user['daily_withdrawals']:.2f} / 1000 AZN")
            print(f"Cash withdrawal remaining:    {1000-current_user['daily_withdrawals']:.2f} AZN")
            print(f"Fee-free cash remaining: {fee_remaining:.2f} AZN")
            print(f"Daily transfers used: {current_user['daily_transfers']} / 5")
            print("====================================")

        # 8. Change Password
        elif choice == "8":
            print("Change Password is selected")
            old_pass = input("Enter your current password: ")
            if old_pass == current_user["password"]:
                new_pass = input("Enter new password: ")
                current_user["password"] = new_pass
                with open(DB_FILE, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                print("\nPassword successfully changed!")
            else:
                print("\nError: Incorrect current password.")

        # 9. Logout
        elif choice == "9":
            print("\nLogged out successfully.")
            break

        # 0. Exit
        elif choice == "0":
            print("\nThank you for using ONURbank. Goodbye!")
            exit()
        else:
            print("\nError: Invalid choice. Please select from the menu.")