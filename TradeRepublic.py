from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TradeRepublic:

    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://app.traderepublic.com/login'


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
        print("begin FillPasswordFields")

        try:
            # Warten, bis alle 4 Passwortfelder sichtbar sind
            inputs = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "codeInput__character"))
            )

            # Die Eingabewerte
            values = ['3', '1', '4', '1']

            # Durch jedes Input-Feld iterieren und die Werte eingeben
            for i, input_field in enumerate(inputs):
                input_field.send_keys(values[i])  # Sendet die entsprechenden Zahlen
                print(f"Zahl {values[i]} in das Feld {i + 1} eingegeben")
                time.sleep(1)

        except Exception as e:
            print(f"Fehler beim Ausfüllen der Passwortfelder: {e}")

    #Logging in to TradeRepublic
    def Login(self):
        self.driver.get(self.url)
        self.HandleCookies()
        self.EnterPhoneNumber()
        self.EnterPin()



