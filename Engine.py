from TradeRepublic import TradeRepublic
from Day import Day
from DBConnector import DBConnector
from Clock import Clock



class Engine:
    def __init__(self, driver):
        self.TradeRepublic = TradeRepublic(driver)
        self.DBConector = DBConnector()
        self.driver = driver


    def start(self):
        self.TradeRepublic.Login()

    def PushProducts(self):
        data = self.TradeRepublic.GetProducts()
        self.DBConector.Startconnection()
        self.DBConector.PushProducts(data[0],data[1])


    def GetDays(self):
        print("Start Getting Dailys, please wait!")
        self.DBConector.Startconnection()
        countedProducts = self.DBConector.GetNumberOfProducts()
        data = self.DBConector.GetProducts()

        for i in range(countedProducts):
            day = Day(data[0][i],data[1][i],data[2][i])
            day.GetDay(self.TradeRepublic)
            day.PushData()


