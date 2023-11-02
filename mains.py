import sqlite3
import random as r
from datetime import datetime
class Bank:
    print("=============================================================")
    print("                 WELCOME TO THEE DECIDERS BANK               ")
    print("=============================================================")
    #inintializing a database
    def __init__(self):
        self.logged_in_user = None
        self.con = sqlite3.connect("Bank.db")   #connect to the database
        self.c = self.con.cursor()              #for allowing the communication between python and sqlite
        
    def CreateAccount(self):       
        self.c.execute("""create table if not exists Bank
            (
                account_name text,
                acc_no integer,
                balance integer,
                password text,
                id_number integer UNIQUE 
            )""")
        self.c.execute("""create table if not exists Transactions
            (
                account_name text,
                transaction_type text,
                amount integer,
                date text
            )""")
        n1 = input("\nEnter Your First Name: ").upper()
        n2 = input("\nEnter Your Last Name: ").upper()
        if n1.isalpha() and not n1.isspace() and n2.isalpha() and not n2.isspace() and len(n1)>2 and len(n2)>2:
            name = n1+" "+n2
            num = r.randint(10000000,99999999)
            
            while True:
                id_number = input("\nEnter your ID number: ")
                if id_number.isdigit() and len(id_number) == 13:
                    break
                else:
                    print("\nInvalid ID number, Please enter a 13 digits number:")
            for row in self.c.execute("select * from Bank where id_number=?", (id_number,)):
                print("\nUser with ID number already exists")
                return
            
            while True:
                password = input("\nCreate a password for your account: ")
                if password.isdigit() and len(password) == 4:
                    break
                else:
                    print("\nInvalid password. Please enter a 4-digit number.")

            while True:
                deposit_amount = float(input("\nDeposit activating amount (R): "))
                if deposit_amount >= 50.00:
                    break
                else:
                    print("\nActivating amount must be R 50.00 or more.")
            
            self.amount = round(deposit_amount,2)
            self.c.execute("insert into Bank values(?,?,?,?,?)",(name,num,self.amount,password,id_number))
            print("\nHello {} Your Account got Created, Note Your Account Number.".format(name))
            print("\nYour Account Number is:- {}".format(num))
            self.con.commit()

        else:
            print("\nEnter Valid Name Surname , Try Again...!")
            
    def CheckBalance(self):
        if self.logged_in_user is not None:
            for a, b, c, p, id_number in self.c.execute("select * from Bank"):
                if a == self.logged_in_user:
                    print(f"\nHello {a}, Your Account Balance is R {c:.2f}")
                    return
        else:
            print("You need to be logged in to check your balance.")

    def Deposit(self):
        if self.logged_in_user is not None:
            min_amount = 10.00
            while True:
                deposit_amount = float(input("\nEnter the amount to deposit: R "))
                if deposit_amount>= min_amount:
                    break
                else:
                    print(f"\nInvalid Deposit amount. Enter amount from R {min_amount} :")

            for a, b, c, p, id_number in self.c.execute("select * from Bank"):
                if a == self.logged_in_user:
                    if deposit_amount>= min_amount:
                        new_balance = round(c + deposit_amount,2)
                        self.c.execute("update Bank set balance = ? where account_name = ?", (new_balance, a))

                        # Record the transaction
                        self.c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?)",
                                (a, "Deposit", deposit_amount, datetime.now().strftime("%Y-%m-%d %H:%M")))

                        print(f"\nDeposit of R {deposit_amount:.2f} successful. New balance is R {new_balance:.2f}")
                        return
                    else:
                        print(f"\n Minimum amount to deposit is R {min_amount}")
        else:
            print("You need to be logged in to deposit money.")

    def Withdraw(self):
        if self.logged_in_user is not None:
            while True:
                withdraw_amount = float(input("\nEnter the amount to withdraw: R "))
                if withdraw_amount>=10:
                    break
                else:
                    print("\nInvalid amount, withdrawal amount starts from R 10.00:")
    
            for a, b, c, p, id_number in self.c.execute("select * from Bank"):
                if a == self.logged_in_user:
                    if c >= withdraw_amount:
                        new_balance = round(c - withdraw_amount,2)
                        self.c.execute("update Bank set balance = ? where account_name = ?", (new_balance, a))
                        # Record the transaction
                        self.c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?)",
                                    (a, "Withdrawal", withdraw_amount, datetime.now().strftime("%Y-%m-%d %H:%M")))

                        self.con.commit()
                        print(f"\nWithdrawal of R {withdraw_amount} successful. New balance is R {new_balance:.2f}")
                    else:
                        print("\nInsufficient funds.")
                    return
        else:
            print("You need to be logged in to withdraw money.")
    
    def ViewUserAccounts(self):
        print("\nExisting User Accounts:")
        print("\n{:<20} {:<15} {:<10} {:<15}".format("Account Name", "Account Number", "Balance", "ID Number"))
        for row in self.c.execute("SELECT * FROM Bank"):
            account_name, acc_no, balance, _, id_number = row  # Ignore password for display
            print("{:<20} {:<15} {:<10} {:<15}".format(account_name, acc_no, balance, id_number))
    
    def ViewTransactions(self):
        if self.logged_in_user is not None:
            print(f"\nTransaction History for {self.logged_in_user}:")
            print("\n{:<20} {:<15} {:<10} {:<20}".format("Account Name", "Transaction", "Amount (R)", "Date"))
            for row in self.c.execute("SELECT * FROM Transactions WHERE account_name=?", (self.logged_in_user,)):
                transaction_type, amount, date, account_name = row
                print("{:<20} {:<15} {:<10} {:<20}".format(transaction_type, amount, date, account_name))
        else:
            print("You need to be logged in to view transactions.")

    def LogIn(self):
        acc_no = int(input("\nEnter Your Account Number or ID Number: "))
        password = input("\nEnter Your Password: ")
        for a, b, c, p, id_number in self.c.execute("select * from Bank"):
            if (b == int(acc_no) or id_number == acc_no) and p == password:
                self.logged_in_user = a
                print(f"\nWelcome {a}! You are now logged in.")
                while True:
                    print("\n----------------------Menu-----------------------")
                    print("\n         1. Check Balance")
                    print("         2. Withdraw Money")
                    print("         3. Deposit Money")
                    print("         4. View Transaction History")
                    print("         5. Log Out")
                    choice = input("\nEnter your choice (1-5): ")
                    if choice == '1':
                        self.CheckBalance()
                    elif choice == '2':
                        self.Withdraw()
                    elif choice == '3':
                        self.Deposit()
                    elif choice == '4':
                        self.ViewTransactions()
                    elif choice == '5':
                        self.LogOut()
                        break
                    else:
                        print("\nInvalid choice. Please try again.")
                break
        else:
            print("\nInvalid Account/ID Number or Password.")
    
    def LogOut(self):
        if self.logged_in_user is not None:
            print(f"\nGoodbye {self.logged_in_user}! You are now logged out.")
            self.logged_in_user = None

            while True:
                print("\n------------------------MENU---------------------------")
                print("\n         1. Create New Account")
                print("         2. Login")
                print("         3. View User Accounts")
                print("         4. Exit")
                print("---------------------------------------------------------")
                choice = input("\nEnter your choice (1-4): ")

                if choice == '1':
                    self.CreateAccount()
                    break
                elif choice == '2':
                    self.LogIn()
                    break
                elif choice == '3':
                    self.ViewUserAccounts()
                    break
                elif choice == '4':
                    exit()
                else:
                    print("\nInvalid choice. Please try again.")
        else:
            print("You are not logged in.")

bk = Bank()

while True:
    print("\n-------------------------- MENU -----------------------------")
    print("\n         1. Create New Account")
    print("         2. Login")
    print("         3. View User Accounts")
    print("         4. Exit")
    print("--------------------------------------------------------------")
    op = input("\nEnter your choice (1-4): ")

    if op == '1':
        bk.CreateAccount()
    elif op == '2':
        bk.LogIn()
    elif op == '3':
        bk.ViewUserAccounts()
        break
    elif op == '4':
        break
    else:
        print("\nInvalid choice. Please try again.")

