import time
import re
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Clock import Clock
from Utils import get_last_5_trading_days

class HeadlessTradeRepublic:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://app.traderepublic.com/login'
        self.prices = []

    def HandleWebDriverSignature(self):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def HandleCookies(self):
        try:
            button = WebDriverWait(self.driver, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/div/div/form/section[2]/button[1]"))
            )
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(f"Cookie-Akzeptanz fehlgeschlagen: {e}")

    def EnterPhoneNumber(self):
        try:
            input_field = WebDriverWait(self.driver, 0.1).until(
                EC.visibility_of_element_located((By.ID, "loginPhoneNumber__input"))
            )
            input_field.clear()
            input_field.send_keys("17663387149")

            button = WebDriverWait(self.driver, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/main/div/div[2]/section/div/div/div/div/form/button"))
            )
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(f"Fehler bei Telefonnummer/Login: {e}")

    def EnterPin(self):
        try:
            pin_inputs = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "codeInput__character"))
            )
            pin_values = ['3', '1', '4', '1']
            for i, pin_field in enumerate(pin_inputs):
                pin_field.send_keys(pin_values[i])
                time.sleep(0.1)

            print("PIN erfolgreich eingegeben. Warte auf SMS-Code...")
            self.WaitForSMSCode()  # <-- hier kommt die Eingabe ins Spiel

        except Exception as e:
            print(f"Fehler beim PIN-Eingeben: {e}")

    def WaitForSMSCode(self):
        print("Bitte SMS-Code eingeben (4 Ziffern, nacheinander):")
        code = input(">>> SMS-Code: ").strip()

        if len(code) != 4 or not code.isdigit():
            print("Ungültiger Code. Bitte genau 4 Ziffern eingeben.")
            return self.WaitForSMSCode()

        try:
            for i in range(4):
                field = self.driver.find_element(By.CSS_SELECTOR, f"#smsCode__input > input:nth-child({i + 2})")
                field.send_keys(code[i])
                time.sleep(0.2)
            print("SMS-Code eingegeben.")
        except Exception as e:
            print(f"Fehler beim Eingeben des SMS-Codes: {e}")

    def Login(self):
        self.driver.get(self.url)
        self.HandleWebDriverSignature()
        self.HandleCookies()
        self.EnterPhoneNumber()
        self.EnterPin()

    def GetReferenceValue(self):
        try:
            el = self.driver.find_element(By.CSS_SELECTOR, "#root > g:nth-child(1) > g.reference-value > g > text")
            return float(el.text.strip().replace('.', '').replace(',', '.'))
        except:
            return None

    def GetRefPx(self):
        try:
            el = self.driver.find_element(By.CSS_SELECTOR, "#root > g:nth-child(1) > g.reference-value > g")
            transform = el.get_attribute("transform")
            return float(transform.split(",")[1].split(")")[0])
        except:
            return None

    def GetMaxPrice(self, child):
        try:
            selector = f"#root > g:nth-child(1) > g.y-axis > g:nth-child({child}) > text"
            val = self.driver.find_element(By.CSS_SELECTOR, selector).text.strip()
            return float(val.replace('.', '').replace(',', '.'))
        except:
            if child > 0:
                return self.GetMaxPrice(child - 1)
            return None

    def convert_prices(self, raw_prices):
        maxVal = self.GetMaxPrice(9)
        ref = self.GetReferenceValue()
        px = self.GetRefPx()
        if None in [maxVal, ref, px]:
            return []
        factor = (maxVal - ref) / px
        return [maxVal - (y * factor) for y in raw_prices]

    def GetPrices(self, reference):
        try:
            path = self.driver.find_element(By.ID, 'chartPriceLine')
            d_attr = path.get_attribute('d')
            coords = re.findall(r'[ML]\s?(\d+\.\d+),(\d+\.\d+)', d_attr)
            y_values = [float(y) for _, y in coords]
            return self.convert_prices(y_values)
        except:
            return []

    def GetDailyTimes(self, prices):
        times = []
        clock = Clock(7, 40)
        for _ in prices:
            times.append(clock.GetTime())
            clock.increaseMinutes(10)
        return times

    def GetWeeklyTimes(self, prices):
        times = []
        days = get_last_5_trading_days()
        idx = 0
        for day_index, day in enumerate(days):
            t = day.replace(hour=7, minute=0, second=0, microsecond=0)
            while t.hour < 22 and idx < len(prices):
                times.append(f"{day_index}:{t.hour}:{t.minute:02d}")
                t += timedelta(minutes=10)
                idx += 1
        return times

    def GetDataFromURI(self, url):
        self.driver.get(url)
        time.sleep(1)
        reference = self.GetReferenceValue()
        if reference is not None:
            return self.GetPrices(reference)
        return []

    def GetProducts(self):
        self.driver.get("https://app.traderepublic.com/browse/stock")
        names, urls = [], []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(10):
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr.tableRow')
            for row in rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, '.instrumentResult__name').text.strip()
                    code = row.find_element(By.CSS_SELECTOR, 'span.instrumentResult__details').get_attribute('innerHTML')
                    urls.append(f"https://app.traderepublic.com/instrument/{code}?timeframe=")
                    names.append(name)
                except:
                    continue
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return [names, urls]
