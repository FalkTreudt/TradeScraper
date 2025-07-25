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
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from HeadlessTradeRepublic import HeadlessTradeRepublic



class Engine:
    def __init__(self):
        self.DBConector = DBConnector()
        self.days = []
        self.dayWorker = []


    def start(self,driver):

        self.TradeRepublic = TradeRepublic(driver)
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

    def getHeadlessDriver(self):
        driver_path = r"C:\Users\Falk\Downloads\edgedriver_win64\msedgedriver.exe"
        service = Service(driver_path)

        options = webdriver.EdgeOptions()
        options.use_chromium = True

        # Headless, Anti-Detection & Benutzer-Agent
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/114.0.0.0 Safari/537.36")

        # WebDriver starten
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def repair_missing_data(self):
        print("🛠️ Repariere fehlende Daten...")
        self.DBConector.Startconnection()
        product_data = self.DBConector.GetProducts()
        ids, names, urls = product_data

        fehlende = self.DBConector.check_missing_ids_in_tables(ids)

        for i, aktie_id in enumerate(ids):
            fehlende_tabs = [t for t in fehlende if aktie_id in fehlende[t]]
            if not fehlende_tabs:
                continue

            name = names[i]
            url = urls[i]

            if "Preise" in fehlende_tabs:
                print(f"→ Tagesdaten fehlen für {name}")
                day = Day(aktie_id, name, url)
                day.GetDay(self.TradeRepublic)
                day.PushData()

            if "PreiseWoche" in fehlende_tabs:
                print(f"→ Wochendaten fehlen für {name}")
                week = Week(aktie_id, name, url)
                week.GetWeek(self.TradeRepublic)
                week.PushData()

            if "PreiseMonat" in fehlende_tabs:
                print(f"→ Monatsdaten fehlen für {name}")
                month = Month(aktie_id, name, url)
                month.GetMonth(self.TradeRepublic)
                month.PushData()

            if "PreiseJahr" in fehlende_tabs:
                print(f"→ Jahresdaten fehlen für {name}")
                year = Year(aktie_id, name, url)
                year.GetYear(self.TradeRepublic)
                year.PushData()

    def create_driver(headless=True):
        driver_path = r"C:\Users\Falk\Downloads\edgedriver_win64\msedgedriver.exe"  # Verwende Raw String (r"") oder doppelten Backslash
        service = Service(driver_path)
        options = webdriver.EdgeOptions()
        options.use_chromium = True  # Edge basiert auf Chromium
        options.add_argument(
            "--disable-blink-features=AutomationControlled")  # Verhindert die Anzeige des WebDriver-Hinweises

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        # WebDriver initialisieren
        driver = webdriver.Edge(service=service, options=options)
        return driver
