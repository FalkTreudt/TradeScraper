from TradeRepublic import TradeRepublic
from Day import Day
from DBConnector import DBConnector
from Clock import Clock
import threading
import time
from Calculator import Calculator



class Engine:
    def __init__(self, driver):
        self.TradeRepublic = TradeRepublic(driver)
        self.DBConector = DBConnector()
        self.driver = driver
        self.days = []
        self.dayWorker = []


    def start(self):
        self.TradeRepublic.Login()

    def PushProducts(self):
        data = self.TradeRepublic.GetProducts()
        self.DBConector.Startconnection()
        self.DBConector.PushProducts(data[0],data[1])


    def GetDays(self):
        self.DBConector.Startconnection()
        countedProducts = self.DBConector.GetNumberOfProducts()
        threads = []

        # Erstellen und starten der Threads
        for i in range(countedProducts):
            thread = threading.Thread(target=self.GetNewDay, name=f"Thread-{i + 1}")
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def GetNewDay(self):
        if True == False:
            print("Start Getting Dailys, please wait!")
            self.DBConector.Startconnection()
            countedProducts = self.DBConector.GetNumberOfProducts()
            data = self.DBConector.GetProducts()

            for i in range(countedProducts):
                day = Day(data[0][i], data[1][i], data[2][i])
                day.GetDay(self.TradeRepublic)
                day.PushData()
        print(f"Thread {threading.current_thread().name} started")
        time.sleep(5)
        print(f"Thread {threading.current_thread().name} finished")

    def GetBestProduct(self):
        calc = Calculator()
        calc.GetDaysFromDB()

        threads = []



        for thread in threads:
            thread.join()


