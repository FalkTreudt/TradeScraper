from selenium import webdriver
from selenium.webdriver.edge.service import Service
from HeadlessTradeRepublic import HeadlessTradeRepublic  # Stelle sicher, dass diese Datei im gleichen Verzeichnis ist
import time

# === 1. WebDriver-Konfiguration ===

def getHeadlessDriver():
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

# === 2. TradeRepublic-Objekt starten ===
tr = HeadlessTradeRepublic(getHeadlessDriver())

# === 3. Login-Prozess starten ===
tr.Login()


