from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Firefox Optionen erstellen
firefox_options = Options()
firefox_options.add_argument('--headless')  # Headless-Modus aktivieren
firefox_options.add_argument('--no-sandbox')  # Verhindert Sandbox-Probleme
firefox_options.add_argument('--disable-dev-shm-usage')  # Verhindert Shared Memory-Probleme

# Geckodriver Service
gecko_driver_path = '/usr/local/bin/geckodriver'  # Standardpfad für Geckodriver
service = Service(gecko_driver_path)

# Firefox WebDriver starten
driver = webdriver.Firefox(service=service, options=firefox_options)

# Beispiel: URL aufrufen
driver.get('https://www.google.com/?hl=de&zx=1751373259440&no_sw_cr=1')

# Beispiel: Alle Links auf der Seite auslesen
links = driver.find_elements(By.TAG_NAME, 'a')

# Alle Links ausdrucken
for link in links:
    href = link.get_attribute('href')
    if href:
        print(f'Link: {href}')

# WebDriver schließen
driver.quit()
