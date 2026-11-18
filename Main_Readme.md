#  ONURbank - Python ATM System

A simple and secure ATM (Banking) system developed in Python as a team project.

##  Team and Responsibilities
This project was collaboratively built by a 3-member team using Git (branching and pull requests):

 Full Name | Responsibilities / Developed Features 

 Abduyev Rahim | Login system, password verification, account blocking, and automatic daily limit reset 
 Həsənov Onur | Deposit, cash withdrawal, and 2% commission calculation mechanism 
 Nurməmməd Qasımov | Inter-account transfers, transaction history (`TXN` IDs), and password change feature 

##  Main Features
* **Authentication & Security:** Password verification, card blocking after 6 failed attempts, and a 60-second cooldown after 3 failures.
* **Balance & Info:** View account details and check real-time balances.
* **Cash Operations:** 
  * Deposit money (daily limit: 2,000 AZN).
  * Withdraw money (daily limit: 1,000 AZN, first 500 AZN fee-free, 2% commission on the excess amount).
* **Inter-Account Transfers:** Transfer money to other users using their account numbers (daily limit: 5 transfers).
* **Transaction History:** Track recent transactions formatted as `TXN0001`.
* **Daily Limits:** Automatic reset of daily limits at the start of a new day.

##  File Structure
* `main.py` - Main ATM application script.
* `bank_data.json` - Local database storing user information (automatically generated).

##  Technologies Used
* Python 3
* JSON
* Git & GitHub

##  Test Accounts
You can use these test accounts to log in after running the application (automatically created on first run):

* **User 1:** `user01` | Password: `Test@123` | Account №: `10010001`
* **User 2:** `user02` | Password: `Test@456` | Account №: `10010002`
* **User 3:** `user03` | Password: `Test@789` | Account №: `10010003`

---
*To run the application, type this command in your terminal:*
```bash
python main.py
