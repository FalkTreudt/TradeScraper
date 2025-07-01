from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Pfad zum Chromium WebDriver angeben
chromium_driver_path = "/usr/lib/chromium-browser/chromedriver"  # Standardpfad für den Chromium WebDriver auf Raspberry Pi

# Chromium Optionen erstellen
chrome_options = Options()

# Falls du den Browser im Headless-Modus (ohne GUI) ausführen möchtest:
chrome_options.add_argument('--headless')  # Optional: Entferne dies, um den Browser mit GUI zu starten

# Service mit dem angegebenen Pfad zum WebDriver
service = Service(chromium_driver_path)

# Webbrowser mit den angegebenen Optionen öffnen
driver = webdriver.Chrome(service=service, options=chrome_options)

# Beispiel: URL aufrufen
driver.get('https://www.google.com/?hl=de&zx=1751373259440&no_sw_cr=1')

# Beispiel: Alle Links auf der Seite auslesen
links = driver.find_elements(By.TAG_NAME, 'a')

for link in links:
    href = link.get_attribute('href')
    if href:
        print(f'Link: {href}')

# Webbrowser schließen
driver.quit()
