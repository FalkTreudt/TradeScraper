from Clock import Clock
from DBConnector import DBConnector
from TradeRepublic import TradeRepublic
from Calculator import Calculator
from Engine import Engine
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from HeadlessTradeRepublic import HeadlessTradeRepublic
import time


driver_path = r"C:\Users\Falk\Downloads\edgedriver_win64\msedgedriver.exe"  # Verwende Raw String (r"") oder doppelten Backslash
service = Service(driver_path)
options = webdriver.EdgeOptions()
options.use_chromium = True  # Edge basiert auf Chromium
options.add_argument("--disable-blink-features=AutomationControlled")  # Verhindert die Anzeige des WebDriver-Hinweises

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# WebDriver initialisieren
#driver = webdriver.Edge(service=service, options=options)

#Link for All Products in TradeRepublic: https://app.traderepublic.com/browse/stock

#Engine = Engine(driver)

#Engine.GetDays()


calc = Calculator()
#calc.GetProducts()

con = DBConnector()
con.Startconnection()
con.GetCurrentWeek()
#con.GetCurrentDays()
calc.GetBestWeekProducts()
calc.GetBestProducts()








#calc.GetBestProducts()




#con.GetCurrentDataFromID(1)

#days = calc.GetDaysFromDB()


#calc.GetBestProducts()

def create_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")  # Für neuere Chrome-Versionen
        options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver