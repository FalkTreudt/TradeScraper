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
            days[i].GetDayFromDB(i+1, data)
        return days


    def CalcRegression(self,day):
        slope  = day.GetSlope()
        return slope

    def GetBestProducts(self):
        print('start Getting Best products')
        self.slopes = [[],[]]
        self.days = self.GetDaysFromDB()
        days = self.days
        print(f'day1 {days[52].name} Preise: {days[52].prices}')

        for i in range(len(self.days)):
            self.days[i].slope = self.CalcRegression(self.days[i])

        max_slope = max(day.slope for day in days)
        best_day = max(days, key=lambda d: d.slope)

        print(f'Maximale Steigung {best_day.slope} bei der ID: {best_day.Aktie_ID} mit den Preisen: {best_day.prices}')
        best_day.DrawDay()
        print(f'Aktie: {best_day.name}')

