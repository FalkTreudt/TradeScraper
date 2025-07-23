from TradeRepublic import TradeRepublic
import plotly.graph_objects as go
from datetime import datetime

class Day:
    def __init__(self, ID, name, URL):
        self.Aktie_ID = ID
        self.name = name
        self.URL = URL + "1d"
        self.prices = []
        self.times = []
        self.slope = 0

    def GetDay(self, tradeRepublic):
        self.prices = tradeRepublic.GetDataFromURI(self.URL)
        self.times = tradeRepublic.GetDailyTimes(self.prices)

    def GetDayFromDB(self, aktie_id, data):
        if aktie_id in data:
            self.prices = [float(p) for p in data[aktie_id]['preise']]
            self.times = data[aktie_id]['zeiten']
        else:
            print(f'Keine Daten für ID {aktie_id} gefunden')
            self.prices = []
            self.times = []

    def DrawDay(self):
        if len(self.prices) == len(self.times) and len(self.prices) > 1:
            times_in_minutes = [self.time_to_minutes(t) for t in self.times]
            m, b = self.GetSlopeForDraw()
            regression_line = [m * x + b for x in times_in_minutes]

            fig = go.Figure(
                data=go.Scatter(x=self.times, y=self.prices, mode='lines+markers', name='Preise')
            )
            fig.add_trace(go.Scatter(x=self.times, y=regression_line, mode='lines',
                                     name='Regressionslinie', line=dict(color='red')))

            fig.update_layout(
                title="Preisentwicklung mit Regressionslinie",
                xaxis_title="Zeit",
                yaxis_title="Preis (€)",
                template="plotly_dark"
            )
            fig.show()

    def time_to_minutes(self, time_input):
        """Konvertiert 'HH:MM' oder datetime → Minuten seit Mitternacht"""
        if isinstance(time_input, datetime):
            return time_input.hour * 60 + time_input.minute
        elif isinstance(time_input, str):
            try:
                time_obj = datetime.strptime(time_input, "%H:%M")
                return time_obj.hour * 60 + time_obj.minute
            except ValueError:
                print(f"Ungültiges Zeitformat: {time_input}")
                return 0
        else:
            print(f"Unbekannter Zeittyp: {type(time_input)}")
            return 0

    def GetSlope(self):
        x = [self.time_to_minutes(t) for t in self.times]
        y = self.prices
        n = len(x)
        if n < 2:
            return -100  # zu wenig Daten

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x_i ** 2 for x_i in x)

        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return -100

        m = (n * sum_xy - sum_x * sum_y) / denominator
        return m

    def GetSlopeForDraw(self):
        x = [self.time_to_minutes(t) for t in self.times]
        y = self.prices
        n = len(x)
        if n < 2:
            return -100, -100

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x_i ** 2 for x_i in x)

        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return -100, -100

        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n
        return m, b

    def PushData(self):
        from DBConnector import DBConnector
        if len(self.prices) == len(self.times):
            connector = DBConnector()
            connector.Startconnection()
            connector.PushDay(self)
            connector.closeConnection()
