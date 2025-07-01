from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from TradeRepublic import TradeRepublic




# Pfad zum Microsoft Edge WebDriver
driver_path = r"C:\Users\Falk\Downloads\edgedriver_win64\msedgedriver.exe"  # Verwende Raw String (r"") oder doppelten Backslash
service = Service(driver_path)
options = webdriver.EdgeOptions()
options.use_chromium = True  # Edge basiert auf Chromium
options.add_argument("--disable-blink-features=AutomationControlled")  # Verhindert die Anzeige des WebDriver-Hinweises

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# WebDriver initialisieren
driver = webdriver.Edge(service=service, options=options)


trade_republic = TradeRepublic(driver)
trade_republic.Login()

# Warten, um sicherzustellen, dass die Seite geladen wird
time.sleep(3)

# Beispiel: Suche ein HTML-Element und interagiere damit (z.B. Eingabefeld)
#input_element = driver.find_element(By.NAME, "q")  # Beispiel: Ein Sucheingabefeld mit dem Namen "q"
#input_element.send_keys("Selenium")  # Gib 'Selenium' in das Eingabefeld ein
#input_element.send_keys(Keys.RETURN)  # Drücke Enter

# Warten, damit das Ergebnis geladen wird
#time.sleep(30)

# Schließe den Browser
#driver.quit()
