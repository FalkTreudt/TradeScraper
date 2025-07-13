import requests
from bs4 import BeautifulSoup

# Hole den HTML-Code von der Seite
url = "https://app.traderepublic.com/instrument/DE0007030009?timeframe=1d"
response = requests.get(url)

# BeautifulSoup verwenden, um den HTML-Code zu parsen
soup = BeautifulSoup(response.text, 'html.parser')

# Suche nach dem gewünschten Wert mit dem CSS-Selektor
reference_value = soup.select_one("#root > g:nth-child(1) > g.reference-value > g > text")

# Überprüfen, ob der Referenzwert gefunden wurde
if reference_value:
    print(f"Gefundener Referenzwert: {reference_value.get_text().strip()}")
else:
    print("Referenzwert nicht gefunden.")
