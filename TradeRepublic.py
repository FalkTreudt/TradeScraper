from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import plotly.graph_objects as go

class TradeRepublic:

    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://app.traderepublic.com/login'

    def HandleWebDriverSignature(self):
        # Manipulation von JavaScript, um "navigator.webdriver" zu falsifizieren
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    #Clicks CookieButton
    def HandleCookies(self):
        print("begin HandleCookies")
        try:
            print('Versuche Cookies zu akzeptieren')

            # Warte, bis der Button mit dem angegebenen XPath sichtbar und klickbar ist (bis zu 20 Sekunden)
            button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/div/div/form/section[2]/button[1]"))
            )

            # Scrollen zum Button, falls es außerhalb des sichtbaren Bereichs ist
            self.driver.execute_script("arguments[0].scrollIntoView();", button)

            # Klicken mit ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(button).click().perform()

            print("Button 'Alle Akzeptieren' wurde geklickt!")

        except Exception as e:
            print(f"Fehler beim Klicken auf den Button: {e}")

    def EnterPhoneNumber(self):
        print("begin EnterPhoneNumber")

        try:
            print("Warten auf das Telefonnummern-Eingabefeld")

            # Warte darauf, dass das Telefonnummern-Eingabefeld sichtbar ist
            phone_input = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, "loginPhoneNumber__input"))
            )

            # Gebe eine Telefonnummer in das Eingabefeld ein
            phone_input.clear()  # Stelle sicher, dass das Eingabefeld zuerst leer ist
            phone_input.send_keys("17663387149")  # Beispielnummer für Deutschland

            print("Telefonnummer eingegeben!")

        except Exception as e:
            print(f"Fehler beim Eingeben der Telefonnummer: {e}")

        print('Start Clicking ContinueButton')

        try:
            print('Versuche den Button zu klicken')

            # Warte, bis der Button klickbar ist (bis zu 20 Sekunden)
            submit_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div[1]/div/main/div/div[2]/section/div/div/div/div/form/button"))
            )

            # Klick auf den Button
            submit_button.click()
            print("Button wurde geklickt!")

        except Exception as e:
            print(f"Fehler beim Klicken auf den Button: {e}")

    def EnterPin(self):
        print("begin HandlePinInput")

        try:
            print("Warten auf die PIN-Eingabefelder")

            # Warte, bis alle 4 PIN-Eingabefelder sichtbar sind
            pin_inputs = WebDriverWait(self.driver, 4).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "codeInput__character"))
            )

            # Die PIN Zahlen
            pin_values = ['3', '1', '4', '1']

            # Gebe die PIN nacheinander ein, mit Verzögerung
            for i, pin_field in enumerate(pin_inputs):
                pin_field.send_keys(pin_values[i])
                time.sleep(0.1)  # Verzögerung für realistischere Eingabe

            print("PIN wurde erfolgreich eingegeben!")

        except Exception as e:
            print(f"Fehler beim Eingeben der PIN: {e}")

    def GetData(self):
        # Warten, bis das Diagramm geladen ist
        try:
            chart = self.driver.find_element(By.ID, 'mainChart')  # Das SVG-Element
        except Exception as e:
            print("Fehler: Das Chart-Element konnte nicht gefunden werden.", e)
            return []  # Falls das Chart-Element nicht gefunden wird, eine leere Liste zurückgeben

        # Extrahieren der 'd'-Eigenschaft des SVG-Pfads, der die Preislinie enthält
        path = self.driver.find_element(By.ID, 'chartPriceLine')
        d_attr = path.get_attribute('d')

        # Extrahieren der X- und Y-Koordinaten aus dem 'd'-Attribut
        # Die 'L' (Linie) und 'M' (Move To) Kommandos enthalten die Koordinaten
        coordinates = re.findall(r'[ML]\s?(\d+\.\d+),(\d+\.\d+)', d_attr)

        # Erstellen von leeren Listen für X-Werte (Zeitpunkte) und Y-Werte (Preise)
        x_values = []
        y_values = []

        # Durch die Koordinaten iterieren und in Listen speichern
        for coord in coordinates:
            x_values.append(float(coord[0]))  # X-Wert (Zeitpunkt)
            y_values.append(float(coord[1]))  # Y-Wert (Preis)

        # Überprüfen, ob überhaupt Werte extrahiert wurden
        if not x_values or not y_values:
            print("Fehler: Keine Koordinaten gefunden.")
            return []  # Leere Liste zurückgeben, falls keine Koordinaten gefunden wurden

        # Optional: Den extrahierten Preis in der Konsole ausgeben
        print(f"X-Werte (Zeitpunkte): {x_values}")
        print(f"Y-Werte (Preise): {y_values}")

        adjusted_values = [3500 - y for y in y_values]

        return y_values  # Nur die Y-Werte (Preise) zurückgeben

    def convert_prices(self,prices):
        # Entfernen des "€"-Symbols und des Tausendertrennzeichens, dann Umwandlung in Fließkommazahlen
        return [float(price.replace(' €', '').replace('.', '').replace(',', '.')) for price in prices]

    def GetReferenceValue(self):
        try:
            # Finde das Element für die Y-Achse
            y_axis = self.driver.find_element(By.CSS_SELECTOR, '.y-axis')

            # Extrahiere alle "tick"-Elemente, die die Skalierung der Y-Achse repräsentieren
            ticks = y_axis.find_elements(By.CSS_SELECTOR, '.tick')

            # Holen wir uns den maximalen Y-Wert aus den Texten der "tick"-Elemente
            y_values = []
            for tick in ticks:
                # Extrahiere den Text (der den Preis darstellen sollte)
                text = tick.text.strip()
                if text:  # Wenn der Text vorhanden ist
                    y_values.append(float(text.replace(',', '.')))  # Um sicherzustellen, dass es eine Zahl ist

            # Berechne den höchsten Y-Wert (der als Referenzwert dient)
            max_y_value = max(y_values) if y_values else None

            if max_y_value:
                print(f"Der dynamisch extrahierte Referenzwert ist: {max_y_value}")
                return max_y_value
            else:
                print("Fehler: Kein maximaler Y-Wert gefunden.")
                return None
        except Exception as e:
            print(f"Fehler beim Extrahieren des Referenzwertes: {e}")
            return None

    def Draw(self,prices):
        # Erstelle x-Werte (Index der Preise)
        x = list(range(len(prices)))

        # Erstelle den Graphen
        fig = go.Figure(data=go.Scatter(x=x, y=prices, mode='lines+markers', name='Preise'))

        # Titel und Achsenbeschriftungen hinzufügen
        fig.update_layout(title="Preisentwicklung",
                          xaxis_title="Zeitpunkte",
                          yaxis_title="Preis (€)",
                          template="plotly_dark")

        # Zeige den Graphen an
        fig.show()

    # Aufruf der Funktion zum Zeichnen des Graphen

    #Logging in to TradeRepublic
    def Login(self):
        self.driver.get(self.url)
        self.HandleWebDriverSignature()
        self.HandleCookies()
        self.EnterPhoneNumber()
        self.EnterPin()
        time.sleep(5)

        data = self.GetData()
        self.Draw(data)

        #print("maxValue = ".  max(data))
        time.sleep(2000)




