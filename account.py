class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan_balance = 0
        self.minimum_balance = 0
        self.frozen = False

    def deposit(self, amount):
        if self.frozen:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit must be positive."
        self.deposits.append(amount)
        return f"Deposited ${amount:.2f}. New balance: ${self.get_balance():.2f}"

    def withdraw(self, amount):
        if self.frozen:
            return "Account is frozen. Cannot withdraw."
        if amount <= 0:
            return "Withdrawal must be positive."
        if self.get_balance() - amount < self.minimum_balance:
            return "Insufficient funds or minimum balance requirement not met."
        self.withdrawals.append(amount)
        return f"Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}"

    def transfer_funds(self, amount, recipient_account):
        if self.frozen:
            return "Account is frozen. Cannot transfer."
        if self.get_balance() - amount < self.minimum_balance:
            return "Insufficient funds or minimum balance requirement not met."
        self.withdrawals.append(amount)
        recipient_account.deposits.append(amount)
        return f"Transferred ${amount:.2f} to {recipient_account.owner}. New balance: ${self.get_balance():.2f}"

    def get_balance(self):
        return sum(self.deposits) - sum(self.withdrawals)

    def request_loan(self, amount):
        if amount <= 0:
            return "Loan amount must be positive."
        self.loan_balance += amount
        self.deposits.append(amount)
        return f"Loan of ${amount:.2f} approved. New balance: ${self.get_balance():.2f}"

    def repay_loan(self, amount):
        if amount <= 0:
            return "Repayment must be positive."
        if self.loan_balance == 0:
            return "You have no loan to repay."
        payment = min(amount, self.loan_balance)
        self.withdrawals.append(payment)
        self.loan_balance -= payment
        return f"Repaid ${payment:.2f} of your loan. Remaining loan: ${self.loan_balance:.2f}"

    def view_account_details(self):
        return f"Owner: {self.owner}\nBalance: ${self.get_balance():.2f}\nLoan Balance: ${self.loan_balance:.2f}"

    def change_account_owner(self, new_owner):
        self.owner = new_owner
        return f"Account owner changed to {new_owner}."

    def account_statement(self):
        print(f"\nStatement for {self.owner}:")
        for i, amount in enumerate(self.deposits, 1):
            print(f"Deposit {i}: +${amount:.2f}")
        for i, amount in enumerate(self.withdrawals, 1):
            print(f"Withdrawal {i}: -${amount:.2f}")
        print(f"Current balance: ${self.get_balance():.2f}")

    def calculate_interest(self):
        if self.frozen:
            return "Account is frozen. Cannot apply interest."
        interest = self.get_balance() * 0.05
        self.deposits.append(interest)
        return f"Interest of ${interest:.2f} applied. New balance: ${self.get_balance():.2f}"

    def freeze_account(self):
        self.frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance must be non-negative."
        self.minimum_balance = amount
        return f"Minimum balance set to ${amount:.2f}"

    def close_account(self):
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan_balance = 0
        return "Account closed. All balances set to zero."


def run_account_menu(account, accounts):
    while True:
        print("\nChoose an operation:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer Funds")
        print("4. Get Balance")
        print("5. Request Loan")
        print("6. Repay Loan")
        print("7. View Account Details")
        print("8. Change Account Owner")
        print("9. Account Statement")
        print("10. Calculate Interest")
        print("11. Freeze Account")
        print("12. Unfreeze Account")
        print("13. Set Minimum Balance")
        print("14. Close Account")
        print("15. Logout")

        choice = input("Enter your choice (1-15): ")

        if choice == '1':
            amount = float(input("Enter deposit amount: "))
            print(account.deposit(amount))

        elif choice == '2':
            amount = float(input("Enter withdrawal amount: "))
            print(account.withdraw(amount))

        elif choice == '3':
            recipient_name = input("Enter recipient's username: ")
            if recipient_name in accounts and accounts[recipient_name] != account:
                amount = float(input("Enter amount to transfer: "))
                print(account.transfer_funds(amount, accounts[recipient_name]))
            else:
                print("Invalid recipient.")

        elif choice == '4':
            print(f"Balance: ${account.get_balance():.2f}")

        elif choice == '5':
            amount = float(input("Enter loan amount: "))
            print(account.request_loan(amount))

        elif choice == '6':
            amount = float(input("Enter amount to repay loan: "))
            print(account.repay_loan(amount))

        elif choice == '7':
            print(account.view_account_details())

        elif choice == '8':
            new_name = input("Enter new owner's name: ")
            print(account.change_account_owner(new_name))

        elif choice == '9':
            account.account_statement()

        elif choice == '10':
            print(account.calculate_interest())

        elif choice == '11':
            print(account.freeze_account())

        elif choice == '12':
            print(account.unfreeze_account())

        elif choice == '13':
            amount = float(input("Enter new minimum balance: "))
            print(account.set_minimum_balance(amount))

        elif choice == '14':
            confirm = input("Are you sure you want to close this account? (yes/no): ")
            if confirm.lower() == 'yes':
                print(account.close_account())
                break

        elif choice == '15':
            print(f"Logged out from {account.owner}'s account.")
            break

        else:
            print("Invalid choice. Try again.")
