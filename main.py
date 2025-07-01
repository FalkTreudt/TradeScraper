from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Chrome-Optionen für Headless-Modus
chrome_options = Options()
chrome_options.add_argument('--headless')  # Keine GUI
chrome_options.add_argument('--no-sandbox')  # Verhindert Fehler durch Sandboxing
chrome_options.add_argument('--disable-dev-shm-usage')  # Verhindert Shared Memory-Probleme

# Pfad zu `chromedriver` auf dem Raspberry Pi
chromedriver_path = '/usr/lib/chromium-browser/chromedriver'

# Starte den WebDriver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

# Beispiel: Besuche eine Webseite
driver.get('https://www.example.com')

# Beispiel: Suche nach einem Element auf der Seite und interagiere damit
# Zum Beispiel ein Eingabefeld ausfüllen
search_box = driver.find_element(By.NAME, 'q')  # Beispiel: Google-Suchfeld
search_box.send_keys('Automatisierungstests mit Selenium')

# Beispiel: Klick auf einen Button (falls vorhanden)
search_button = driver.find_element(By.NAME, 'btnK')  # Beispiel: Google Suchbutton
search_button.click()

# Warte ein paar Sekunden, um die Interaktion abzuschließen
time.sleep(3)

# Beispiel: Extrahiere alle Links von der Seite
links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
    href = link.get_attribute('href')
    if href:
        print(f'Gefundener Link: {href}')

# Schließe den WebDriver
driver.quit()
