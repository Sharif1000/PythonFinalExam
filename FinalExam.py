from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    enable_loan = True
    is_bankrupt = False

    def __init__(self, name, email, address, accountType):
        self.name = name
        self.email = email
        self.address = address
        self.accountNo = name + '-' + email
        self.balance = 0
        self.accountType = accountType
        self.loan_taken = 0
        self.loan_taken_amount = 0
        self.transactions = []
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited {amount} tk")
            print(f"Deposited {amount} tk. New balance: {self.balance} tk")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if Account.is_bankrupt == False:
            if amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    self.transactions.append(f"Withdrew {amount} tk")
                    print(f"Withdrew {amount} tk. New balance: {self.balance} tk")
                else:
                    print("Withdrawal amount exceeded")
            else:
                print("Invalid withdrawal amount")
        else:
            print("Bank is Bankrupt")

    def check_balance(self):
        print(f"Available balance: {self.balance} tk")

    def transaction_history(self):
        print("Transaction History:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        if self.loan_taken < 2 and Account.enable_loan:
            self.balance += amount
            self.loan_taken += 1
            self.loan_taken_amount += amount
            self.transactions.append(f"Loan taken: {amount} tk")
            print(f"{amount} tk taken successfully as Loan.")
        else:
            print("You have already taken the maximum number of loans or loan feature is disabled.")

    def transfer(self, amount, recipient_account):
        if amount > 0:
            if amount <= self.balance:
                recipient_account.deposit(amount)
                self.balance -= amount
                self.transactions.append(f"Transferred {amount} tk to account {recipient_account.accountNo}")
                print(f"Transferred {amount} tk to account {recipient_account.accountNo}")
            else:
                print("Insufficient balance for transfer")
        else:
            print("Invalid transfer amount")

    @abstractmethod
    def show_info(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, email, address, interestRate):
        super().__init__(name, email, address, "Savings")
        self.interestRate = interestRate

    def apply_interest(self):
        interest = self.balance * (self.interestRate / 100)
        self.balance += interest
        self.transactions.append(f"Deposited {interest} tk as interest")
        print(f"Deposited {interest} tk as interest. New balance: {self.balance} tk")

    def show_info(self):
        print(f"Account Information:")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Type: {self.accountType}")
        print(f"Account Number: {self.accountNo}")
        print(f"Balance: {self.balance} tk")


class CurrentAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Current")

    def show_info(self):
        print(f"Account Information:")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Type: {self.accountType}")
        print(f"Account Number: {self.accountNo}")
        print(f"Balance: {self.balance} tk")


class Admin:
    @staticmethod
    def create_account(name, email, address, account_type, interest_rate=None):
        if account_type.upper() == "SV":
            new_account = SavingsAccount(name, email, address, interest_rate)
        elif account_type.upper() == "CR":
            new_account = CurrentAccount(name, email, address)
        else:
            print("Invalid account type.")
            return None
        return new_account

    @staticmethod
    def delete_account(account_no):
        for i, account in enumerate(Account.accounts):
            if account.accountNo == account_no:
                del Account.accounts[i]
                print(f"Account {account_no} deleted successfully.")
                return
        print("Account not found.")

    @staticmethod
    def see_all_accounts():
        if len(Account.accounts) > 0:
            print("All User Accounts:")
            for account in Account.accounts:
                print(f"Account Number: {account.accountNo}, Name: {account.name}, Email: {account.email}")
        else:
            print("No accounts found.")

    @staticmethod
    def check_total_balance():
        total_balance = sum(account.balance for account in Account.accounts)
        print(f"Total Available Balance of the Bank: {total_balance} tk")

    @staticmethod
    def check_total_loan_amount():
        total_loan_amount = sum(account.loan_taken_amount for account in Account.accounts)
        print(f"Total Loan Amount: {total_loan_amount} tk")

    @staticmethod
    def toggle_loan_feature(enable_loan):
        Account.enable_loan = enable_loan
        status = ""
        if enable_loan == True:
            status = "enabled"
        else:
            status = "disabled"
        print(f"Loan Feature of the Bank is now {status}.")
        
    @staticmethod
    def toggle_is_bankrupt(toggle):
        Account.is_bankrupt = toggle

# Main program
currentUser = None
admin_mode = False

while True:
    if currentUser is None and not admin_mode:
        print("\nNo user logged in!")
        ch = input("\nRegister/Login (R/L) Admin Mode (A): ")

        if ch.upper() == "R":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            account_type = input("Account Type (SV/CR): ")

            if account_type.upper() == "SV":
                ir = int(input("Interest rate: "))
                currentUser = SavingsAccount(name, email, address, ir)
            elif account_type.upper() == "CR":
                currentUser = CurrentAccount(name, email, address)
            else:
                print("Invalid account type.")

        elif ch.upper() == "L":
            account_no = input("Account Number: ")
            for account in Account.accounts:
                if account.accountNo == account_no:
                    currentUser = account
                    break

        elif ch.upper() == "A":
            admin_name = input("admin Name: ")
            admin_password = input("admin Password: ")
            if admin_name == "admin" and admin_password == "123":
                admin_mode = True
            
        else:
            print("Invalid choice.")

    elif admin_mode == True:
        print("\nAdmin Mode:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. See All User Accounts")
        print("4. Check Total Available Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature (On/Off)")
        print("7. Toggle Bankrupt Feature (On/Off)")
        print("8. Exit Admin Mode")

        admin_choice = input("Choose Option: ")

        if admin_choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            account_type = input("Account Type (SV/CR): ")
            if account_type.upper() == "SV":
                ir = int(input("Interest rate: "))
                Admin.create_account(name, email, address, account_type, ir)
            elif account_type.upper() == "CR":
                Admin.create_account(name, email, address, account_type)
            else:
                print("Invalid account type.")

        elif admin_choice == "2":
            account_no = input("Enter account number to delete: ")
            Admin.delete_account(account_no)

        elif admin_choice == "3":
            Admin.see_all_accounts()

        elif admin_choice == "4":
            Admin.check_total_balance()

        elif admin_choice == "5":
            Admin.check_total_loan_amount()

        elif admin_choice == "6":
            enable_loan = input("Do you want to enable loan feature? (yes/no): ").lower()
            if enable_loan == "yes":
                Admin.toggle_loan_feature(True)
            elif enable_loan == "no":
                Admin.toggle_loan_feature(False)
            else:
                print("Invalid input.")
                
        elif admin_choice == "7":
            bankrupt = input("Do you want to enable bankrupt feature? (yes/no): ").lower()
            if bankrupt == "yes":
                Admin.toggle_is_bankrupt(True)
            elif bankrupt == "no":
                Admin.toggle_is_bankrupt(False)
            else:
                print("Invalid input.")

        elif admin_choice == "8":
            admin_mode = False

        else:
            print("Invalid choice.")
    else:
        print(f"\nWelcome {currentUser.name}!\n")

        if currentUser.accountType == "Savings":
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transaction History")
            print("5. Take Loan")
            print("6. Transfer Money")
            print("7. Apply Interest")
            print("8. Show Information")
            print("9. Logout\n")

            choice = input("Choose Option: ")

            if choice == "1":
                amount = int(input("Enter deposit amount: "))
                currentUser.deposit(amount)

            elif choice == "2":
                amount = int(input("Enter withdrawal amount: "))
                currentUser.withdraw(amount)

            elif choice == "3":
                currentUser.check_balance()

            elif choice == "4":
                currentUser.transaction_history()

            elif choice == "5":
                amount = int(input("Enter loan amount: "))
                currentUser.take_loan(amount)

            elif choice == "6":
                recipient_account_no = input("Enter recipient account number: ")
                recipient_account = None
                for account in Account.accounts:
                    if account.accountNo == recipient_account_no:
                        recipient_account = account
                        break
                if recipient_account:
                    amount = int(input("Enter transfer amount: "))
                    currentUser.transfer(amount, recipient_account)
                else:
                    print("Recipient account does not exist.")

            elif choice == "7":
                currentUser.apply_interest()

            elif choice == "8":
                currentUser.show_info()

            elif choice == "9":
                currentUser = None

            else:
                print("Invalid choice.")

        else:
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transaction History")
            print("5. Take Loan")
            print("6. Transfer Money")
            print("7. Show Information")
            print("8. Logout\n")

            choice = input("Choose Option: ")

            if choice == "1":
                amount = int(input("Enter deposit amount: "))
                currentUser.deposit(amount)

            elif choice == "2":
                amount = int(input("Enter withdrawal amount: "))
                currentUser.withdraw(amount)

            elif choice == "3":
                currentUser.check_balance()

            elif choice == "4":
                currentUser.transaction_history()

            elif choice == "5":
                amount = int(input("Enter loan amount: "))
                currentUser.take_loan(amount)

            elif choice == "6":
                recipient_account_no = input("Enter recipient account number: ")
                recipient_account = None
                for account in Account.accounts:
                    if account.accountNo == recipient_account_no:
                        recipient_account = account
                        break
                if recipient_account:
                    amount = int(input("Enter transfer amount: "))
                    currentUser.transfer(amount, recipient_account)
                else:
                    print("Recipient account does not exist.")

            elif choice == "7":
                currentUser.show_info()

            elif choice == "8":
                currentUser = None

            else:
                print("Invalid choice.")

    
