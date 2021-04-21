import sqlite3
from all_classes import *
import datetime
import sys

conn = sqlite3.connect('STOCK_EXCHANGE.db')
"""
if conn:
    print("Database successfully created")


stock_exchange = '''CREATE TABLE Stock_Exchange(
    id INT PRIMARY KEY AUTO INCREMENT NOT NULL,
    established_date DATETIME NOT NULL,
    number_of_companies INT
)
'''

broker = '''CREATE TABLE Broker(
    id INT AUTO_INCREMENT PRIMARY KEY,
    verified_by NOT NULL,
    name VARCHAR(20) NOT NULL,
    FOREIGN KEY(verified_by) REFERENCES Stock_Exchange(id) 
)
'''
conn.execute(broker)
trader = '''CREATE TABLE Trader(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password VARCHAR(30) NOT NULL,
    available_funds FLOAT
)
'''
conn.execute(trader)
stock = '''CREATE TABLE Stock(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    face_value FLOAT NOT NULL,
    current_price FLOAT NOT NULL,
    number_of_stocks INT NOT NULL
)
'''
conn.execute(stock)
owns = '''CREATE TABLE Owns(
    Id INT NOT NULL,
    stock_id INT NOT NULL,
    number_of_stocks INT NOT NULL,
    FOREIGN KEY(Id) REFERENCES Trader(id),
    FOREIGN KEY(stock_id) REFERENCES Stock(id)
)
'''
conn.execute(owns)
buy=''' CREATE TABLE BuyOrder(
    Id INT NOT NULL,
    stock_id INT NOT NULL,
    number_of_stocks INT NOT NULL,
    sell_price FLOAT NOT NULL,
    FOREIGN KEY(sell_price) REFERENCES Stock(current_price),
    FOREIGN KEY(Id) REFERENCES Trader(id),
    FOREIGN KEY(stock_id) REFERENCES Stock(id)
)
'''
conn.execute(buy)
sell=''' CREATE TABLE SellOrder(
    Id INT NOT NULL,
    stock_id INT NOT NULL,
    number_of_stocks INT NOT NULL,
    sell_price FLOAT NOT NULL,
    FOREIGN KEY(sell_price) REFERENCES Stock(current_price),
    FOREIGN KEY(Id) REFERENCES Trader(id),
    FOREIGN KEY(stock_id) REFERENCES Stock(id)
)
'''
conn.execute(sell)
listed_stocks = '''CREATE TABLE Listed_Stocks(
    id INT NOT NULL,
    listed_under INT NOT NULL,
    FOREIGN KEY(id) REFERENCES Stock(id),
    FOREIGN KEY(listed_under) REFERENCES Stock_Exchange(id)
)
'''
conn.execute(listed_stocks)
conn.execute("ALTER TABLE Stock_Exchange ADD name VARCHAR(20)")

"""

"""
t="SELECT * FROM Stock_Exchange"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM Broker"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM Stock"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM Trader"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM Owns"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM BuyOrder"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM SellOrder"
t1= list(conn.execute(t))
print(t1)
print()

t="SELECT * FROM Listed_Stocks"
t1= list(conn.execute(t))
print(t1)
print()
"""


def get_all_owned_by_trader(user_id):
    q= "SELECT Stock.name , Owns.number_of_stocks FROM Owns JOIN Stock On Stock.id = Owns.stock_id WHERE Owns.Id = ?"
    res = list(conn.execute(q,(user_id,)))
    return res

def insert_into_stocks(stock):
    insert_stock = "INSERT INTO Stock(id,name,face_value,current_price,number_of_stocks) VALUES(?,?,?,?,?)"
    conn.execute(insert_stock,(stock.stock_id,stock.company_name,stock.face_value,stock.current_price,stock.number_of_stocks))
    conn.execute("UPDATE Stock_Exchange SET number_of_companies = number_of_companies + 1")
    conn.commit()

def get_all_stocks():
    all_stocks = list(conn.execute("SELECT name,current_price,number_of_stocks FROM Stock"))
    return all_stocks

def number_of_listed_companies():
    for cnt in conn.execute("SELECT number_of_companies FROM Stock_Exchange"):
        return cnt[0]

def delete_stock(stock_name):

    res= list(conn.execute("SELECT id FROM Stock WHERE name=  ?",(stock_name,)))
    res1=list(conn.execute("SELECT Id,number_of_stocks FROM Owns WHERE stock_id = ?",(res[0][0],)))
    for i in res1:
        sell_obj = SellOrder(res[0][0],i[1],i[0])
        res = sell_stock_order(sell_obj)
 
    conn.execute("DELETE FROM Stock WHERE name = ?",(stock_name,))
    conn.execute("UPDATE Stock_Exchange SET number_of_companies = number_of_companies - 1")
    #print(res1)
    conn.commit()


def get_all_transactions_of_user(user_id):
    #buys = list(conn.execute("SELECT * FROM BuyOrder WHERE id = ?",(user_id,)))
    q= "SELECT Stock.name , BuyOrder.number_of_stocks FROM BuyOrder JOIN Stock On Stock.id = BuyOrder.stock_id WHERE BuyOrder.Id = ?"
    #sells = list(conn.execute("SELECT * FROM SellOrder WHERE id = ?",(user_id,)))
    q2 = "SELECT Stock.name,SellOrder.number_of_stocks FROM SellOrder JOIN Stock On Stock.id = SellOrder.stock_id WHERE SellOrder.Id = ?"
    #all_trs = dict()
    #all_trs["buy_orders"] = buys
    #all_trs["sell_orders"] = sells
    res = dict()
    res['buys'] = list(conn.execute(q,(user_id,)))
    res['sells'] = list(conn.execute(q2,(user_id,)))
    return res


def get_stock_exchange_details():
    res = conn.execute("SELECT number_of_companies,established_date FROM Stock_Exchange ")
    for det in res:
        return det

def add_trader(trader):
    x = len(list(conn.execute("SELECT * FROM Trader")))
    x = 200 + (x+1)
    query = "INSERT INTO Trader(id,name,email,password,available_funds) VALUES(?,?,?,?,?)"
    conn.execute(query,(x,trader.username,trader.email,trader.password,trader.funds_available))
    conn.commit()

    return True
    



def buy_stock_order(buy_stock):
    funds = list(conn.execute("SELECT available_funds FROM Trader WHERE id = ?",(buy_stock.trader,)))
    funds = float(funds[0][0])
    curr_price = list(conn.execute("SELECT current_price from Stock WHERE id = ?",(buy_stock.stock,)))
    curr_price = float(curr_price[0][0])
    if funds < (curr_price*buy_stock.number_of_stocks_to_trade) :
        raise Exception("Insufficient funds!")
    else:
        
        s = list(conn.execute("SELECT number_of_stocks FROM Stock WHERE id = ?",(buy_stock.stock,)))
        s = float(s[0][0])
        if s >= buy_stock.number_of_stocks_to_trade:
            av = s-buy_stock.number_of_stocks_to_trade
            avf = funds - (curr_price*buy_stock.number_of_stocks_to_trade)
            query = "INSERT INTO BuyOrder(Id,stock_id,number_of_stocks,sell_price) VALUES(?,?,?,?)"
            conn.execute(query,(buy_stock.trader,buy_stock.stock,buy_stock.number_of_stocks_to_trade,curr_price,))
            check_already_have = list(conn.execute("SELECT * FROM Owns WHERE Id = ? AND stock_id = ?",(buy_stock.trader,buy_stock.stock)))
            if check_already_have:
                conn.execute("UPDATE Owns SET number_of_stocks = number_of_stocks + ? WHERE Id = ? AND stock_id = ?",
                (buy_stock.number_of_stocks_to_trade,buy_stock.trader,buy_stock.stock))
            else:
                conn.execute("INSERT INTO Owns(Id,stock_id,number_of_stocks) VALUES(?,?,?)",
                (buy_stock.trader,buy_stock.stock,buy_stock.number_of_stocks_to_trade))

            conn.execute("UPDATE Stock SET number_of_stocks=? WHERE id=?",
            (av,buy_stock.stock))
            conn.execute("UPDATE Trader SET available_funds=?  WHERE id=?",
            (avf,buy_stock.trader))
            conn.commit()
            return True
        else:
            print("buying stock quantity is grater than available stock quantity")
            return False

def sell_stock_order(sell_stock):
    owned = list(conn.execute("SELECT number_of_stocks FROM Owns WHERE Id = ? AND stock_id=?",
    (sell_stock.trader,sell_stock.stock)))
    if not owned :
        return False
    owned = int(owned[0][0])
    if owned < sell_stock.number_of_stocks_to_trade :
        raise Exception("Insufficient stocks available!")
    else:
        s = list(conn.execute("SELECT number_of_stocks FROM Stock WHERE id = ?",(sell_stock.stock,)))
        s = float(s[0][0])
        curr_price = list(conn.execute("SELECT current_price from Stock WHERE id = ?",(sell_stock.stock,)))
        curr_price = float(curr_price[0][0])
        query = "INSERT INTO SellOrder(Id,stock_id,number_of_stocks,sell_price) VALUES(?,?,?,?)"
        conn.execute(query,(sell_stock.trader,sell_stock.stock,sell_stock.number_of_stocks_to_trade,curr_price))
        left = owned - sell_stock.number_of_stocks_to_trade
        conn.execute("UPDATE Owns SET number_of_stocks = ? WHERE Id = ? AND stock_id = ?",
                (left,sell_stock.trader,sell_stock.stock))
        conn.execute("UPDATE Stock SET number_of_stocks = number_of_stocks + ? WHERE id = ?",
            (sell_stock.number_of_stocks_to_trade,sell_stock.stock))
        conn.execute("UPDATE Trader SET available_funds = available_funds + ? WHERE id = ?",
            (sell_stock.number_of_stocks_to_trade*curr_price,sell_stock.trader))
        conn.commit()
        return True

def return_portfolio(user_id):
    res = dict()
    orders = get_all_transactions_of_user(user_id)
    res["orders"] = orders

    res["current_owns"] = get_all_owned_by_trader(user_id)
    res["Available_funds"] = float(list(conn.execute("SELECT available_funds FROM Trader WHERE id=?",(user_id,)))[0][0])
    return res

def get_stock_id(name):
    res = list(conn.execute("SELECT id from STOCK WHERE name = ?",(name,)))
    if res:
        return res[0][0]
    else:
        return False


def get_user(em,passwd):
    user = list(conn.execute("SELECT * FROM Trader WHERE email=? AND password=?",(em,passwd)))
    return user

def get_exchange(exchange_name,exchange_id):
    user = list(conn.execute("SELECT * FROM Stock_Exchange WHERE name=? AND id=?",(exchange_name,exchange_id)))
    #print(user[0])
    return user[0]


#get_exchange("BSE",1)


"""
ril = Stock(1002,"RIL",12,5000,20000000)
icici = Stock(1003,"ICICI",2,355,1500000)
airtel = Stock(1004,"AIRTEL",15,255,35000000)
at = Stock(1008,"ADANI TRANSMISSION",9,512,55500000)
insert_into_stocks(at)
vi = Stock(1009,"VI",12,19,105000000)
insert_into_stocks(vi)
sbi = Stock(1010,"SBI",2,1234,10900000)
insert_into_stocks(sbi)
axis = Stock(1011,"AXIS",5,20,15000000)
insert_into_stocks(axis)
ca = Stock(1012,"CRAFTSMAN AUTOMATION",7,113,15000000)
insert_into_stocks(ca)
ar = Stock(1013,"ANUPAM RASAYAN",15,543,22000000)
insert_into_stocks(ar)
insert_into_stocks(icici)gn key
insert_into_stocks(airtel)
conn.execute("ALTER TABLE Trader ADD broker_id INT NOT NULL DEFAULT(100)")
all_stocks = get_all_stocks()
c = number_of_listed_companies()
se = get_stock_exchange_details()
print("Trader",list(conn.execute("SELECT * FROM Trader")))
print("Broker",list(conn.execute("SELECT * FROM Broker")))
print("Owns",list(conn.execute("SELECT * FROM Owns")))
print("trs",get_all_transactions_of_user(201))
print(se)
print(all_stocks)
print(c)
print("Owns",list(conn.execute("SELECT * FROM Owns")))
sell = SellOrder(1010,1,201)
sell_stock_order(sell)
print("Owns",list(conn.execute("SELECT * FROM Owns")))
pt = return_portfolio(201)
print(pt)
"""
