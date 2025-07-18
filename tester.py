from Clock import Clock
from DBConnector import DBConnector
from TradeRepublic import TradeRepublic
from Calculator import Calculator


calc = Calculator()
#calc.GetProducts()

con = DBConnector()
con.Startconnection()

days = calc.GetDaysFromDB()


calc.GetBestProducts()