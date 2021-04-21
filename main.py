import sys
from all_db import *
from all_classes import *
from getpass import getpass


def login():
    email = input("Enter your email : ")
    password = getpass("Enter your password : ")
    user = get_user(email,password)
    if not user:
        print("User doesn't exist or wrong credentials entered, Try again!")
        return None
    return user[0]

def register():
    name = input("Enter your name : ")
    email = input("Enter your email : ")
    funds = float(input("Enter the funds : "))
    password = getpass("Enter your password : ")
    password2 = getpass("Confirm password : ")
    if password == password2 and name and email:
        user = Trader(name,email,password,100,funds)
        add_trader(user)
        user = get_user(email,password)
        #print(user)
        return user[0]
    
    else:
        print("Trader registration failed!")


print()
print("1. Trader Register")
print("2. Trader Log In")
print("3. Admin login")
print()


choice = int(input("Enter your choice : "))
user = None


def show_exchange_options():
    print()
    print("1. Add new companies")
    print("2. Delete companies") 
    print("3. Show Listed Companies Details")
    print("4. exit")
    print()

if choice ==3 :
    exchange_name = input("Enter the exchange name")
    exchange_id = int(input("Enter the exchange id "))
    ex=get_exchange(exchange_name,exchange_id)
    if not ex :
        print("exchange doesn't exist or wrong credentials entered, Try again!")
        
    else:
        while(True):
            show_exchange_options()
            option = int(input("Enter Your Choice : "))
            print()
            if option==1:
                id=int(input("enter the ID of the company"))
                company_name=input("enter the name of the company")
                face_value=float(input("enter the face value of the stock"))
                current_price=float(input("enter the current price of the stock"))
                number_of_stocks=int(input("enter the number of stocks"))
                new = Stock(id,company_name,face_value,current_price,number_of_stocks)
                insert_into_stocks(new)
            elif option == 2 :
                company_name=input("enter the name of the company to delete")
                delete_stock(company_name)
            elif option == 3 :
                all_stocks = get_all_stocks()
                name = "Company Name"
                curr_price = "Current Price"
                available = "Available Stocks"
                print()
                print(f'{name:25}\t\t{curr_price:25}\t\t{available:25}')
                for stock in all_stocks :
                    print(f'{stock[0]:<25}\t\t{stock[1]:<25}\t\t{stock[2]:<25}')
            elif option == 4:
                print()
                print("\t\t\t----Happy Trading----")
                print()
                exit()
            else: 
                continue





if choice == 1 :
    user = register()

elif choice == 2 :
    user = login()
all_user_details = dict()

if user:
    all_user_details['id'] = int(user[0])
    all_user_details['name'] = user[1]
    all_user_details['email'] = user[2]
    all_user_details['password'] = user[3]
    all_user_details['available_funds'] = int(user[4])
    all_user_details['broker_id'] = user[-1]


def show_options():
    print()
    print("1. Buy Stocks")
    print("2. Sell Stocks") 
    print("3. Show Portfolio")
    print("4. Show Transactions")
    print("5. Show Listed Companies")
    print("6. Log Out")
    print()

if not user:
    exit()

while True:
    show_options()
    option = int(input("Enter Your Choice : "))
    print()


    if option == 1 :

        cname = input("Enter Company Name : ")
        sid = get_stock_id(cname)
        if sid:
            n = int(input("Enter number of stocks you want to buy : "))
        else:
            print("company name does not exist")
            continue

        buy_obj = BuyOrder(sid,n,all_user_details['id'])
        res = buy_stock_order(buy_obj)
        if res :
            print("Order placed successfully")
            print()
            print(get_all_owned_by_trader(all_user_details['id']))
            print()
        else:
            print("Order not successful")

    elif option == 2 :
        cname = input("Enter Company Name : ")
        sid = get_stock_id(cname)
        if sid:
            n = int(input("Enter number of stocks you want to sell : "))
        sell_obj = SellOrder(sid,n,all_user_details['id'])
        res = sell_stock_order(sell_obj)
        if res:
            print("Order Placed Successfully")
            #   print(get_all_owned_by_trader(all_user_details['id']))
            print()
        else:
            print("order not successful")



    elif option == 3 :
        portfolio = return_portfolio(all_user_details['id'])
        print()
        for key,value in portfolio.items() :
            print(f"<<--------- {key} --------->>")
            print()
            print(f"{value}")
            print()

        print()
    
    elif option == 4 :
        trs = get_all_transactions_of_user(all_user_details['id'])
        print()
        print("\t\t\tBuy Orders : ")
        print()
        cname = "Company"
        no = "Number of Stocks Traded"
        print(f'{cname:<25}\t\t{no:<25}')
        if trs['buys'] : 
            for orders in trs['buys']:
                print(f'{orders[0]:<25}\t\t{orders[1]:<25}')

        print()
        print("\t\t\tSell Orders : ")
        print()
        if trs['sells']:
            print(f'{cname:<25}\t\t{no:<25}')
            for orders in trs['sells']:
                print(f'{orders[0]:<25}\t\t{orders[1]:<25}')




    elif option == 5 :
        all_stocks = get_all_stocks()
        name = "Company Name"
        curr_price = "Current Price"
        available = "Available Stocks"
        print()
        print(f'{name:25}\t\t{curr_price:25}\t\t{available:25}')
        for stock in all_stocks :
            print(f'{stock[0]:<25}\t\t{stock[1]:<25}\t\t{stock[2]:<25}')

    else:
        all_user_details = None
        print()
        print("\t\t\t----Happy Trading----")
        print()
        break


conn.commit()
conn.close()