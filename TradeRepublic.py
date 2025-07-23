import time
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Clock import Clock
import plotly.graph_objects as go
from datetime import datetime, timedelta
import Utils


class TradeRepublic:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://app.traderepublic.com/login'
        self.prices = []

    def HandleWebDriverSignature(self):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def HandleCookies(self):
        try:
            print('Versuche Cookies zu akzeptieren')
            button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/div/div/form/section[2]/button[1]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            ActionChains(self.driver).move_to_element(button).click().perform()
            print("Cookies akzeptiert.")
        except Exception as e:
            print(f"Fehler beim Klicken auf den Cookie-Button: {e}")

    def EnterPhoneNumber(self):
        try:
            phone_input = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "loginPhoneNumber__input"))
            )
            phone_input.clear()
            phone_input.send_keys("17663387149")
            print("Telefonnummer eingegeben.")

            submit_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/main/div/div[2]/section/div/div/div/div/form/button"))
            )
            submit_button.click()
            print("Login-Button geklickt.")
        except Exception as e:
            print(f"Fehler bei Telefonnummer oder Login-Button: {e}")

    def EnterPin(self):
        try:
            pin_inputs = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "codeInput__character"))
            )
            pin_values = ['3', '1', '4', '1']
            for i, pin_field in enumerate(pin_inputs):
                pin_field.send_keys(pin_values[i])
                time.sleep(0.1)

            while self.driver.current_url == 'https://app.traderepublic.com/login':
                time.sleep(1)

            print("PIN erfolgreich eingegeben.")
        except Exception as e:
            print(f"Fehler beim PIN-Eingeben: {e}")

    def Login(self):
        self.driver.get(self.url)
        self.HandleWebDriverSignature()
        self.HandleCookies()
        self.EnterPhoneNumber()
        self.EnterPin()
        time.sleep(1)

    def GetPrices(self, reference):
        try:
            chart = self.driver.find_element(By.ID, 'mainChart')
        except Exception as e:
            print("Fehler: Chart nicht gefunden.", e)
            return []

        try:
            path = self.driver.find_element(By.ID, 'chartPriceLine')
            d_attr = path.get_attribute('d')
            coordinates = re.findall(r'[ML]\s?(\d+\.\d+),(\d+\.\d+)', d_attr)

            x_values = [float(coord[0]) for coord in coordinates]
            y_values = [float(coord[1]) for coord in coordinates]

            if not y_values:
                print("Keine Preis-Koordinaten gefunden.")
                return []

            return self.convert_prices(y_values)

        except Exception as e:
            print(f"Fehler beim Extrahieren der Preise: {e}")
            return []

    def convert_prices(self, prices):
        print('Starte Preis-Konvertierung')
        maxVal = self.GetMaxPrice(9)
        refPx = self.GetRefPx()
        ref = self.GetReferenceValue()

        if None in [maxVal, refPx, ref]:
            print("Fehlerhafte Werte zur Preisumrechnung (max, ref, px)")
            return []

        factor = (maxVal - ref) / refPx
        converted = [maxVal - (p * factor) for p in prices]
        print('Konvertierte Preise:', converted)
        return converted

    def GetDailyTimes(self, prices):
        times = []
        clock = Clock(7, 40)
        for _ in prices:
            times.append(clock.GetTime())
            clock.increaseMinutes(10)
        return times

    def GetWeeklyTimes(self, prices):
        print("Starting WeeklyTimes with Handelszeiten")
        times = []
        days = get_last_5_trading_days()  # liefert datetime-Objekte für die letzten 5 Handelstage

        current_index = 0
        for day_index, day in enumerate(days):
            current_time = day.replace(hour=7, minute=0, second=0, microsecond=0)
            end_time = day.replace(hour=22, minute=0)

            while current_time < end_time and current_index < len(prices):
                # Format: "0:9:00"
                tag = day_index  # 0 = ältester Handelstag
                stunde = current_time.hour
                minute = current_time.minute
                times.append(f"{tag}:{stunde}:{minute:02d}")
                current_time += timedelta(minutes=10)
                current_index += 1

            if current_index >= len(prices):
                break

        return times


    def GetReferenceValue(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "#root > g:nth-child(1) > g.reference-value > g > text")
            value = element.text.strip().replace('.', '').replace(',', '.')
            return float(value)
        except Exception as e:
            print(f"Fehler beim Referenzwert: {e}")
            return None

    def GetRefPx(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "#root > g:nth-child(1) > g.reference-value > g")
            transform_value = element.get_attribute("transform")
            if "translate" in transform_value:
                y_value = transform_value.split("translate(")[1].split(",")[1].split(")")[0]
                return float(y_value)
            else:
                print("Kein translate-Wert in transform.")
                return None
        except Exception as e:
            print(f"Fehler bei RefPx: {e}")
            return None

    def GetMaxPrice(self, child):
        try:
            selector = f"#root > g:nth-child(1) > g.y-axis > g:nth-child({child}) > text"
            value = self.driver.find_element(By.CSS_SELECTOR, selector).text.strip()
            value = value.replace('.', '').replace(',', '.')
            return float(value)
        except Exception:
            if child > 0:
                return self.GetMaxPrice(child - 1)
            print("MaxPrice nicht gefunden.")
            return None

    def GetDataFromURI(self, url):
        print(f'Lese Daten von: {url}')
        self.driver.get(url)
        time.sleep(1)
        reference = self.GetReferenceValue()
        if reference is not None:
            prices = self.GetPrices(reference)
        else:
            print(f'Kein Referenzwert bei {url} gefunden.')
            prices = []
        return prices

    def GetProducts(self):
        print("Lade Produktliste...")
        self.driver.get('https://app.traderepublic.com/browse/stock')
        stocksName = []
        stocksURL = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for _ in range(10):
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr.tableRow')
            previous_count = len(stocksName)

            for row in rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, '.instrumentResult__name').text.strip()
                    url_code = row.find_element(By.CSS_SELECTOR, 'span.instrumentResult__details').get_attribute('innerHTML')
                    full_url = f'https://app.traderepublic.com/instrument/{url_code}?timeframe='
                    stocksName.append(name)
                    stocksURL.append(full_url)
                except Exception as e:
                    print(f"Fehler bei einer Zeile: {e}")

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or len(stocksName) == previous_count:
                break
            last_height = new_height

        print("Produkte gesammelt:", len(stocksName))
        return [stocksName, stocksURL]
