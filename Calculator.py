from Day import Day
from Week import Week
from DBConnector import DBConnector
from TradeRepublic import TradeRepublic
from concurrent.futures import ThreadPoolExecutor

class Calculator:
    def __init__(self):
        self.TopProducts = []
        self.connector = DBConnector()
        self.connector.Startconnection()
        self.products = self.connector.GetProducts()  # [IDs, names, URLs]

    def GetProducts(self):
        return self.products

    def GetDaysFromDB(self):
        print('Start Getting Day From DB')
        ids, names, urls = self.products
        days = [Day(ids[i], names[i], urls[i]) for i in range(len(ids))]

        data = self.connector.GetCurrentDays()

        for day in days:
            day.GetDayFromDB(day.Aktie_ID, data)

        return days

    def GetWeeksFromDB(self):
        print('Start Getting Week From DB')
        ids, names, urls = self.products
        weeks = [Week(ids[i], names[i], urls[i]) for i in range(len(ids))]

        data = self.connector.GetCurrentWeek()

        for week in weeks:
            week.GetWeekFromDB(week.Aktie_ID, data)

        return weeks

    def CalcRegression(self, day_or_week):
        return day_or_week.GetSlope()

    def GetBestProducts(self):
        print('Start Getting Best Products (Daily)')
        self.days = self.GetDaysFromDB()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.CalcRegression, day) for day in self.days]
            for i, future in enumerate(futures):
                self.days[i].slope = future.result()

        best_day = max(self.days, key=lambda d: d.slope)
        print(f'Maximale Steigung {best_day.slope} bei der ID: {best_day.Aktie_ID} mit den Preisen: {best_day.prices}')
        best_day.DrawDay()
        print(f'Aktie: {best_day.name}')

    def GetBestWeekProducts(self):
        print('Start Getting Best Products (Weekly)')
        self.Weeks = self.GetWeeksFromDB()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.CalcRegression, week) for week in self.Weeks]
            for i, future in enumerate(futures):
                self.Weeks[i].slope = future.result()

        best_week = max(self.Weeks, key=lambda w: w.slope)
        print(f'Maximale Steigung {best_week.slope} bei der ID: {best_week.Aktie_ID} mit den Preisen: {best_week.prices}')
        best_week.DrawWeek()
        print(f'Aktie: {best_week.name}')
