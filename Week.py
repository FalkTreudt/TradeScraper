from TradeRepublic import TradeRepublic
from DBConnector import DBConnector
import plotly.graph_objects as go
from datetime import datetime

class Week:
    def __init__(self, ID, name,URL):
        self.prices = []
        self.times = []
        self.name = name
        self.URL = URL + "5d"
        self.Aktie_ID = self.GetProductID(name)
        self.slope = 0


    def GetWeek(self,tradeRepublic):
        self.prices = tradeRepublic.GetDataFromURI(self.URL)
        self.times = tradeRepublic.GetWeeklyTimes(self.prices)
    def GetWeekFromDB(self,index,data):
        data = data
        if index in data:
            self.prices = [float(p) for p in data[index]['preise']]
            self.times = data[index]['zeiten']
        else:
            print(f'index: {index} nicht vorhanden')
            self.prices =[]
            self.times =[]




    def DrawWeek(self):
        if len(self.prices) == len(self.times):
            # Berechnung der Regressionslinie mit den Text-Zeitangaben
            times_in_minutes = [self.time_to_minutes(time) for time in self.times]

            # Berechne die lineare Regression
            m, b = self.GetSlopeForDraw()

            # Berechne die Y-Werte für die Regressionslinie
            regression_line = [m * x + b for x in times_in_minutes]

            # Erstellen des Plots
            fig = go.Figure(
                data=go.Scatter(x=self.times, y=self.prices, mode='lines+markers', name='Preise'))

            # Füge die Regressionslinie hinzu
            fig.add_trace(go.Scatter(x=self.times, y=regression_line, mode='lines', name='Regressionslinie',
                                     line=dict(color='red')))

            # Titel und Achsenbeschriftungen hinzufügen
            fig.update_layout(title="Preisentwicklung mit Regressionslinie",
                              xaxis_title="Zeitpunkte",
                              yaxis_title="Preis (€)",
                              template="plotly_dark")

            # Zeige den Graphen an
            fig.show()

    def time_to_minutes(self, time_str):
        """Konvertiert eine Zeit im Format HH:MM in Minuten seit Mitternacht"""
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.hour * 60 + time_obj.minute

    def GetSlope(self):

        x = [self.time_to_minutes(time) for time in self.times]
        y = self.prices
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum([x[i] * y[i] for i in range(n)])
        sum_x2 = sum([x_i ** 2 for x_i in x])

        if (n * sum_x2 - sum_x ** 2) != 0:
            # Berechne die Steigung (m) und den Y-Achsenabschnitt (b)
            m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            return m
        else:
            return (-100)


    def GetSlopeForDraw(self):
        x = [self.time_to_minutes(time) for time in self.times]
        y = self.prices
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum([x[i] * y[i] for i in range(n)])
        sum_x2 = sum([x_i ** 2 for x_i in x])

        # Berechne die Steigung (m) und den Y-Achsenabschnitt (b)
        if (n * sum_x2 - sum_x ** 2)!= 0 and n != 0:
            m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            b = (sum_y - m * sum_x) / n
            return m, b
        else:
            return (-100),(-100)
    def GetProductID(self,name):
        connector = DBConnector()
        connector.Startconnection()
        return connector.GetProductID(name)


    def PushData(self):
        if len(self.prices) == len(self.times):
            connector = DBConnector()
            connector.Startconnection()
            connector.PushWeek(self)
            #connector.GetNewID()
            connector.closeConnection()

