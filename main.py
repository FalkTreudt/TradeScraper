from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Pfad zum Chromium WebDriver angeben
chromium_driver_path = '/usr/lib/chromium-browser/chromedriver'  # Standardpfad für Chromium WebDriver auf Raspberry Pi

# Chromium Optionen erstellen
chrome_options = Options()
chrome_options.add_argument('--headless')  # Headless-Modus aktivieren
chrome_options.add_argument('--no-sandbox')  # Verhindert Sandbox-Probleme
chrome_options.add_argument('--disable-dev-shm-usage')  # Verhindert Probleme bei Shared Memory
chrome_options.add_argument('--remote-debugging-port=9222')  # Optional für Debugging

# Service mit dem angegebenen Pfad zum WebDriver
service = Service(chromium_driver_path)

# Webbrowser mit den angegebenen Optionen öffnen
driver = webdriver.Chrome(service=service, options=chrome_options)

# Beispiel: URL aufrufen
driver.get('https://app.traderepublic.com/login')

# Beispiel: Alle Links auf der Seite auslesen
links = driver.find_elements(By.TAG_NAME, 'a')

# Alle Links ausdrucken
for link in links:
    href = link.get_attribute('href')
    if href:
        print(f'Link: {href}')

# Webbrowser schließen
driver.quit()
