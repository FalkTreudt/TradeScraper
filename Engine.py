from TradeRepublic import TradeRepublic
from Day import Day
from Week import Week
from Month import Month
from Year import Year
from DBConnector import DBConnector
from Clock import Clock
import threading
import time
from Calculator import Calculator

from HeadlessTradeRepublic import HeadlessTradeRepublic



class Engine:
    def __init__(self, driver):
        self.TradeRepublic = TradeRepublic(driver)
        self.DBConector = DBConnector()
        self.driver = driver
        self.days = []
        self.dayWorker = []


    def start(self):
        self.TradeRepublic.Login()
        self.DBConector.Startconnection()

    def PushProducts(self):
        data = self.TradeRepublic.GetProducts()
        self.DBConector.PushProducts(data[0],data[1])


    def GetDays(self):
        countedProducts = self.DBConector.GetNumberOfProducts()
        threads = []

        # Erstellen und starten der Threads
        for i in range(countedProducts):
            thread = threading.Thread(target=self.GetNewDay, name=f"Thread-{i + 1}")
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def GetNewDay(self):
            print("Start Getting Dailys, please wait!")
            countedProducts = self.DBConector.GetNumberOfProducts()
            data = self.DBConector.GetProducts()

            for i in range(countedProducts):
                day = Day(data[0][i], data[1][i], data[2][i])
                day.GetDay(self.TradeRepublic)
                day.PushData()

    def CollectDayData(self):
        productInformation = self.DBConector.GetProducts()
        print(f'Produkt informationen {productInformation}')
        days = []
        #len(productInformation[0])
        for i in range(len(productInformation[0])):
            days.append(Day(productInformation[0][i],productInformation[1][i],productInformation[2][i]))

        for day in days:
            day.GetDay(self.TradeRepublic)
            day.PushData()
    def CollectWeekData(self):
        productInformation = self.DBConector.GetProducts()
        print(f'Produkt informationen {productInformation}')
        weeks = []
        #len(productInformation[0])
        for i in range(len(productInformation[0])):
            weeks.append(Week(productInformation[0][i],productInformation[1][i],productInformation[2][i]))

        for week in weeks:
            week.GetWeek(self.TradeRepublic)
            week.PushData()

    def CollectMonthData(self):
        productInformation = self.DBConector.GetProducts()
        print(f'Produktinformationen für Monat: {productInformation}')
        months = []

        for i in range(len(productInformation[0])):
            months.append(Month(productInformation[0][i],
                                productInformation[1][i],
                                productInformation[2][i]))

        for month in months:
            month.GetMonth(self.TradeRepublic)
            month.PushData()

    def CollectYearData(self):
        productInformation = self.DBConector.GetProducts()
        print(f'Produktinformationen für Jahr: {productInformation}')
        years = []

        for i in range(len(productInformation[0])):
            years.append(Year(
                productInformation[0][i],  # ID
                productInformation[1][i],  # Name
                productInformation[2][i]  # URL
            ))

        for year in years:
            year.GetYear(self.TradeRepublic)
            year.PushData()




