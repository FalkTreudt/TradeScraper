from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

# Pfad zum Microsoft Edge WebDriver
driver_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # Ersetze dies mit dem tatsächlichen Pfad zum Edge WebDriver

# Service für den WebDriver initialisieren
service = Service(driver_path)

# WebDriver-Optionen
options = webdriver.EdgeOptions()
options.use_chromium = True  # Edge basiert auf Chromium

# WebDriver initialisieren
driver = webdriver.Edge(service=service, options=options)

# Öffne eine Webseite
driver.get("https://app.traderepublic.com/login")  # Ersetze dies durch die URL, mit der du interagieren möchtest

# Warten, um sicherzustellen, dass die Seite geladen wird
time.sleep(3)

# Beispiel: Suche ein HTML-Element und interagiere damit (z.B. Eingabefeld)
input_element = driver.find_element(By.NAME, "q")  # Beispiel: Ein Sucheingabefeld mit dem Namen "q"
input_element.send_keys("Selenium")  # Gib 'Selenium' in das Eingabefeld ein
input_element.send_keys(Keys.RETURN)  # Drücke Enter

# Warten, damit das Ergebnis geladen wird
time.sleep(3)

# Schließe den Browser
driver.quit()
