from Day import Day
from DBConnector import DBConnector
from TradeRepublic import TradeRepublic


class Calculator:
    def __init__(self):
        self.TopProducts = []
        self.connector = DBConnector()
        self.connector.Startconnection()

    def GetProducts(self):
        products = self.connector.GetProducts()
        return products

    def GetDaysFromDB(self):
        print('Start Getting Day From DB')
        products = self.GetProducts()
        days = []
        for i in range(len(products[0])):
            newDay = Day(products[0][i],products[1][i],products[0][i])
            days.append(newDay)

        return days

    def CalcRegression(self,day):
        slope  = day.GetSlope()
        return slope

    def GetBestProducts(self):
        print('start Getting Best products')
        slopes = []
        days = self.GetDaysFromDB()
        for i in range(len(days)):
            days[i].GetDayFromDB(self.connector)
            slopes.append(self.CalcRegression(days[i]))
        print(f'Maximale Steigung {max(slopes)} bei der ID: {slopes.index(max(slopes))}')
        days[slopes.index(max(slopes))].DrawDay()
        print(f'Aktie: {days[slopes.index(max(slopes))].name}')

