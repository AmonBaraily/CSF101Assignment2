import random
import string

class Account:
    def __init__(self, account_number, balance=0, account_type="", password=""):
        #Start account with account number, balnce, account type, and password
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.password = password

    def check_balance(self):
        # Process to check account balance
        return self.balance

    def deposit(self, amount):
        #Process to deposit money into account
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        # Process to withdraw money from the account
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            return True

    def transfer_money(self, recipient_account, amount):
        # Process to transfer money from this account to another account
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            return True

    def delete_account(self, accounts):
        # Process to delete the account
        accounts.remove(self)
        save_accounts_to_file(accounts)
        print(f"Account {self.account_number} deleted successfully.")

class PersonalAccount(Account):
    def __init__(self, account_number, balance=0, password=""):
         # Constructor for personal account
        super().__init__(account_number, balance, "Personal", password)

class BusinessAccount(Account):
    def __init__(self, account_number, balance=0, password=""):
        # Constructor for business account
        super().__init__(account_number, balance, "Business", password)

def generate_account_number():
     # Function to generate a random account number
    return ''.join(random.choices(string.digits, k=10))

def create_account(account_type, initial_deposit=0):
     # Function to create a new account
    account_number = generate_account_number()
    password = input("Set a password for your account: ")
    if account_type == "personal":
        return PersonalAccount(account_number, initial_deposit, password)
    elif account_type == "business":
        return BusinessAccount(account_number, initial_deposit, password)

def login(account_number, password):
    # Function to login to an existing account
    accounts = load_accounts_from_file()
    for account in accounts:
        if account.account_number == account_number and account.password == password:
            return account
    return None

def save_accounts_to_file(accounts):
    # Function to save accounts to a file
    with open("accounts.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.account_number},{account.balance},{account.account_type},{account.password}\n")

def load_accounts_from_file():
     # Function to load accounts from a file
    accounts = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file.readlines():
                account_info = line.strip().split(",")
                account_type = account_info[2]
                if account_type == "Personal":
                    account = PersonalAccount(account_info[0], float(account_info[1]), account_info[3])
                elif account_type == "Business":
                    account = BusinessAccount(account_info[0], float(account_info[1]), account_info[3])
                accounts.append(account)
    except FileNotFoundError:
        pass
    return accounts

def find_account_by_number(account_number, accounts):
     # Function to find an account by its account number
    for account in accounts:
        if account.account_number == account_number:
            return account
    return None

def main():
    # Main function to run the program
    accounts = load_accounts_from_file()

    while True:
        action = input("Enter action (create, login, transfer, delete, exit): ").lower()
        if action == "create":
            # Create a new account
            account_type = input("Enter account type (personal/business): ").lower()
            initial_deposit = float(input("Enter initial deposit: "))
            new_account = create_account(account_type, initial_deposit)
            accounts.append(new_account)
            save_accounts_to_file(accounts)
            print(f"New account {new_account.account_number} created.")
        elif action == "login":
            # Login to an existing account
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            logged_in_account = login(account_number, password)
            if logged_in_account:
                print(f"Logged in to account {logged_in_account.account_number}.")
                # Add menu options for logged-in account
            else:
                print("Invalid credentials.")
        elif action == "transfer":
            # Transfer money between accounts
            sender_account_number = input("Enter sender account number: ")
            receiver_account_number = input("Enter receiver account number: ")
            amount = float(input("Enter transfer amount: "))
            sender_account = find_account_by_number(sender_account_number, accounts)
            receiver_account = find_account_by_number(receiver_account_number, accounts)
            if sender_account and receiver_account:
                if sender_account.transfer_money(receiver_account, amount):
                    save_accounts_to_file(accounts)
                    print("Transfer successful.")
                else:
                    print("Transfer failed.")
            else:
                print("Invalid account numbers.")
        elif action == "delete":
             # Delete an account
            account_number = input("Enter account number to delete: ")
            password = input("Enter password: ")
            account_to_delete = login(account_number, password)
            if account_to_delete:
                account_to_delete.delete_account(accounts)
            else:
                print("Invalid credentials or account not found.")
        elif action == "exit":
             # Exit the program++
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
