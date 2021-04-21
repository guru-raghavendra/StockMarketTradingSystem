class Trader:
	def __init__(self,name,email,password,broker_id,funds=0):
		self.username = name
		self.email = email
		self.password = password
		self.funds_available = funds
		self.broker_id = broker_id
	
class Stock:
	def __init__(self,id,company_name,face_value,current_price,number_of_stocks):
		self.stock_id = id
		self.company_name = company_name
		self.face_value = face_value
		self.current_price = current_price
		self.number_of_stocks = number_of_stocks
		
class StockExchange:
	def __init__(self,established_date,number_of_listed_companies,id):
		self.id = id
		self.established_date = established_date
		self.number_of_listed_companies = number_of_listed_companies
		
class StockBroker:
	def __init__(self,name,id,verified_by):
		self.broker_name = name
		self.verified_by = verified_by
		self.traders = []
		
		
class BuyOrder:
	def __init__(self,stock,number_of_stocks,trader):
		self.number_of_stocks_to_trade = number_of_stocks
		self.trader = trader
		self.stock = stock
		
	
	
class SellOrder:
	def __init__(self,stock,number_of_stocks,trader):
		self.number_of_stocks_to_trade = number_of_stocks
		self.trader = trader
		self.stock = stock
		
 
		
		
