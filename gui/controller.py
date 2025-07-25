# gui/controller.py
from Engine import Engine
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from HeadlessTradeRepublic import HeadlessTradeRepublic

class EngineController:
    def __init__(self):
        self.engine = Engine()

    def start_engine(self):
        print("🔄 Starte Engine...")
        self.engine.start(getDriver())

    def push_products(self):
        print("📦 Produkte abrufen & speichern...")
        self.engine.PushProducts()

    def collect_day_data(self):
        print("📅 Tagesdaten abrufen...")
        self.engine.CollectDayData()

    def collect_week_data(self):
        print("📈 Wochendaten abrufen...")
        self.engine.CollectWeekData()

    def collect_month_data(self):
        print("🗓️ Monatsdaten abrufen...")
        self.engine.CollectMonthData()

    def collect_year_data(self):
        print("📊 Jahresdaten abrufen...")
        self.engine.CollectYearData()

def getDriver():
    # Pfad zum Microsoft Edge WebDriver
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

    # Link for All Products in TradeRepublic: https://app.traderepublic.com/browse/stock

    return driver