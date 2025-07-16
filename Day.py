from TradeRepublic import TradeRepublic



class Day:
    def __init__(self, name, URL,tradeRepublic):
        self.prices = []
        self.times = []
        self.name = name
        self.URL = URL
        self.tradeRepublic = tradeRepublic

    def GetDay(self):
        self.prices = self.tradeRepublic.GetDataFromURI(self.URL)
        self.times = self.tradeRepublic.GetDailyTimes(self.prices)

        #print(f"Preise: {self.prices} Länge: {len(self.times)}")
        #print(f"Zeiten: {self.times} Länge: {len(self.times)}")

        print(f"Preise: {self.prices}")
        print(f"Zeiten: {self.times}")