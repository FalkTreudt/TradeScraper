from TradeRepublic import TradeRepublic
from DBConnector import DBConnector
class Day:
    def __init__(self, name, URL,tradeRepublic):
        self.prices = []
        self.times = []
        self.name = name
        self.URL = URL
        self.tradeRepublic = tradeRepublic
        self.Aktie_ID = 1

    def GetDay(self):
        self.prices = self.tradeRepublic.GetDataFromURI(self.URL)
        self.times = self.tradeRepublic.GetDailyTimes(self.prices)

        print(f"Preise: {self.prices}")
        print(f"Zeiten: {self.times}")
    def DrawDay(self):
        if len(self.prices) == len(self.times):
            self.tradeRepublic.Draw(self.prices,self.times)

    def PushData(self):
        if len(self.prices) == len(self.times):
            connector = DBConnector()
            connector.Startconnection()
            #connector.PushDay(self)
            connector.GetNewID()
            connector.closeConnection()
