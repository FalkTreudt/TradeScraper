from Day import Day
from DBConnector import DBConnector
from TradeRepublic import TradeRepublic
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class Calculator:
    def __init__(self):
        self.TopProducts = []
        self.connector = DBConnector()
        self.connector.Startconnection()
        self.semaphore = threading.Semaphore(10)

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
        data = self.connector.GetCurrentDays()
        for i in range(len(days)):
            days[i].GetDayFromDB(i, data)

        return days


    def CalcRegression(self,day):
        slope  = day.GetSlope()
        return slope

    def GetBestProducts(self):
        print('start Getting Best products')
        self.slopes = []
        self.days = self.GetDaysFromDB()

        print(f'Länge von Days: {len(self.days)}')

        for i in range(len(self.days)):
            self.slopes.append(self.CalcRegression(self.days[i]))

        print(f'Maximale Steigung {max(self.slopes)} bei der ID: {self.slopes.index(max(self.slopes))}')
        self.days[self.slopes.index(max(self.slopes))].DrawDay()
        print(f'Aktie: {self.days[self.slopes.index(max(self.slopes))].name}')

