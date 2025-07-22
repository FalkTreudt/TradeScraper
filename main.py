from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from TradeRepublic import TradeRepublic
from Day import Day
from Engine import Engine
from DBConnector import DBConnector



# Pfad zum Microsoft Edge WebDriver
driver_path = r"C:\Users\Falk\Downloads\edgedriver_win64\msedgedriver.exe"  # Verwende Raw String (r"") oder doppelten Backslash
service = Service(driver_path)
options = webdriver.EdgeOptions()
options.use_chromium = True  # Edge basiert auf Chromium
options.add_argument("--disable-blink-features=AutomationControlled")  # Verhindert die Anzeige des WebDriver-Hinweises

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# WebDriver initialisieren
driver = webdriver.Edge(service=service, options=options)

#Link for All Products in TradeRepublic: https://app.traderepublic.com/browse/stock

Engine = Engine(driver)
Engine.start()
#Engine.PushProducts()
Engine.CollectWeekData()



# Warten, um sicherzustellen, dass die Seite geladen wird
time.sleep(3000)


#time.sleep(30)

#driver.quit()
