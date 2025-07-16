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

        print(f"Preise: {len(self.prices)}")
        print(f"Zeiten: {len(self.times)}")
    def DrawDay(self):
        self.tradeRepublic.Draw(self.prices,self.times)