from Day import Day
from Week import Week
from Month import Month
from Year import Year
from DBConnector import DBConnector
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

    def GetMonthsFromDB(self):
        print('Start Getting Month From DB')
        ids, names, urls = self.products
        months = [Month(ids[i], names[i], urls[i]) for i in range(len(ids))]

        data = self.connector.GetCurrentMonth()

        for month in months:
            month.GetMonthFromDB(month.Aktie_ID, data)

        return months

    def CalcRegression(self, day_week_or_month):
        return day_week_or_month.GetSlope()

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

    def GetBestMonthProducts(self):
        print('Start Getting Best Products (Monthly)')
        self.Months = self.GetMonthsFromDB()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.CalcRegression, month) for month in self.Months]
            for i, future in enumerate(futures):
                self.Months[i].slope = future.result()

        best_month = max(self.Months, key=lambda m: m.slope)
        print(f'Maximale Steigung {best_month.slope} bei der ID: {best_month.Aktie_ID} mit den Preisen: {best_month.prices}')
        best_month.DrawMonth()
        print(f'Aktie: {best_month.name}')

    def GetYearsFromDB(self):
        print('Start Getting Year From DB')
        ids, names, urls = self.products
        years = [Year(ids[i], names[i], urls[i]) for i in range(len(ids))]

        data = self.connector.GetCurrentYear()

        for year in years:
            year.GetYearFromDB(year.Aktie_ID, data)

        return years

    def GetBestYearProducts(self):
        print('Start Getting Best Products (Monthly)')
        self.Years = self.GetYearsFromDB()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.CalcRegression, year) for year in self.Years]
            for i, future in enumerate(futures):
                self.Years[i].slope = future.result()

        best_year = max(self.Years, key=lambda m: m.slope)
        print(f'Maximale Steigung {best_year.slope} bei der ID: {best_year.Aktie_ID} mit den Preisen: {best_year.prices}')
        best_year.DrawYear()
        print(f'Aktie: {best_year.name}')

