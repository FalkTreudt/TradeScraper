from Day import Day
from Week import Week
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
            newDay = Day(products[0][i],products[1][i],products[2][i])
            days.append(newDay)
        data = self.connector.GetCurrentDays()
        for i in range(len(days)):
            days[i].GetDayFromDB(i+1, data)
        return days
    def GetWeeksFromDB(self):
        print('Start Getting Day From DB')
        products = self.GetProducts()
        weeks = []
        for i in range(len(products[0])):
            newWeek = Week(products[0][i],products[1][i],products[2][i])
            weeks.append(newWeek)
        data = self.connector.GetCurrentWeek()
        for i in range(len(weeks)):
            weeks[i].GetWeekFromDB(i+1, data)
        return weeks


    def CalcRegression(self,day):
        slope  = day.GetSlope()
        return slope

    def GetBestProducts(self):
        print('start Getting Best products')
        self.slopes = [[],[]]
        self.days = self.GetDaysFromDB()
        days = self.days

        for i in range(len(self.days)):
            self.days[i].slope = self.CalcRegression(self.days[i])

        max_slope = max(day.slope for day in days)
        best_day = max(days, key=lambda d: d.slope)

        print(f'Maximale Steigung {best_day.slope} bei der ID: {best_day.Aktie_ID} mit den Preisen: {best_day.prices}')
        best_day.DrawDay()
        print(f'Aktie: {best_day.name}')
    def GetBestWeekProducts(self):
        print('start Getting Best products')
        self.slopes = [[],[]]
        self.Weeks = self.GetWeeksFromDB()
        weeks = self.Weeks

        for i in range(len(self.Weeks)):
            self.Weeks[i].slope = self.CalcRegression(self.Weeks[i])

        max_slope = max(day.slope for day in weeks)
        best_week = max(weeks, key=lambda d: d.slope)

        print(f'Maximale Steigung {best_week.slope} bei der ID: {best_week.Aktie_ID} mit den Preisen: {best_week.prices}')
        best_week.DrawWeek()
        print(f'Aktie: {best_week.name}')
