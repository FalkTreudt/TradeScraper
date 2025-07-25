from DBConnector import DBConnector
from datetime import datetime, timedelta
import plotly.graph_objects as go

class Year:
    def __init__(self, ID, name, URL):
        self.prices = []
        self.times = []
        self.name = name
        self.URL = URL + "1y"
        self.Aktie_ID = ID
        self.slope = 0
        self.trading_days = get_last_trading_days()
        self.percent_change = None
        self.r_squared = None

    def GetYear(self, tradeRepublic):
        self.prices = tradeRepublic.GetDataFromURI(self.URL)
        self.trading_days = get_last_trading_days()
        self.times = self.generate_year_times(len(self.prices))

    def generate_year_times(self, n):
        times = []
        clock = YearClock(self.trading_days)
        for _ in range(n):
            times.append(clock.get_current_time())
            clock.increase()
        return times

    def GetYearFromDB(self, aktie_id, data):
        self.trading_days = get_last_trading_days()
        if aktie_id in data:
            self.prices = [float(p) for p in data[aktie_id]['preise']]
            self.times = data[aktie_id]['zeiten']
        else:
            print(f'Aktie-ID {aktie_id} nicht vorhanden')
            self.prices = []
            self.times = []

    def time_to_minutes(self, time_input):
        if isinstance(time_input, datetime):
            base = self.trading_days[0].replace(hour=0, minute=0, second=0, microsecond=0)
            return int((time_input - base).total_seconds() / 60)
        return 0

    def GetSlope(self):
        """Lineare Regression auf prozentuale Preisveränderung (%/Minute)."""
        if len(self.prices) < 2 or len(self.prices) != len(self.times):
            return -100

        base_price = self.prices[0]
        if base_price == 0:
            return -100

        x = [self.time_to_minutes(t) for t in self.times]
        y = [(p - base_price) / base_price * 100 for p in self.prices]  # Prozentuale Veränderung

        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)

        denom = n * sum_x2 - sum_x ** 2
        if denom == 0:
            return -100

        m = (n * sum_xy - sum_x * sum_y) / denom
        return m  # in Prozent pro Minute

    def GetSlopeForDraw(self):
        x = [self.time_to_minutes(t) for t in self.times]
        y = self.prices
        if len(x) != len(y) or not x:
            return -100, -100

        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)
        denom = n * sum_x2 - sum_x ** 2

        if denom == 0:
            return -100, -100

        m = (n * sum_xy - sum_x * sum_y) / denom
        b = (sum_y - m * sum_x) / n
        return m, b

    def DrawYear(self):
        if len(self.prices) != len(self.times):
            print("Unterschiedliche Länge von Preisen und Zeiten")
            return

        x = [self.time_to_minutes(t) for t in self.times]
        m, b = self.GetSlopeForDraw()
        regression_line = [m * xi + b for xi in x]
        x_labels = [t.strftime("%d.%m.%Y") for t in self.times]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_labels, y=self.prices, mode='lines+markers', name='Preise'))
        fig.add_trace(go.Scatter(x=x_labels, y=regression_line, mode='lines', name='Regression', line=dict(color='red')))

        fig.update_layout(title=f"Preisentwicklung (Jahr) – {self.name}",
                          xaxis_title="Datum",
                          yaxis_title="Preis (€)",
                          template="plotly_dark")
        fig.show()

    def PushData(self):
        if len(self.prices) == len(self.times):
            connector = DBConnector()
            connector.Startconnection()
            connector.PushYear(self)  # du musst PushYear in DBConnector implementieren
            connector.closeConnection()

    def GetPercentChange(self):
        if self.percent_change is not None:
            return self.percent_change

        if not self.prices or len(self.prices) < 2:
            self.percent_change = 0.0
        else:
            start = self.prices[0]
            end = self.prices[-1]
            if start == 0:
                self.percent_change = 0.0
            else:
                self.percent_change = (end - start) / start

        return self.percent_change

    def GetRSquared(self):
        if self.r_squared is not None:
            return self.r_squared

        x = [self.time_to_minutes(t) for t in self.times]
        y = self.prices

        if len(x) != len(y) or not x:
            self.r_squared = 0.0
            return self.r_squared

        n = len(x)
        mean_y = sum(y) / n
        ss_tot = sum((yi - mean_y) ** 2 for yi in y)

        m, b = self.GetSlopeForDraw()
        ss_res = sum((y[i] - (m * x[i] + b)) ** 2 for i in range(n))

        self.r_squared = 0.0 if ss_tot == 0 else max(0.0, min(1.0, 1 - (ss_res / ss_tot)))
        return self.r_squared


def get_last_trading_days(today=None):
    if today is None:
        today = datetime.today()

    one_year_ago = today - timedelta(days=365)
    current = one_year_ago
    trading_days = []

    while current <= today:
        if current.weekday() < 5:  # Montag–Freitag
            trading_days.append(current.replace(hour=12, minute=0, second=0, microsecond=0))
        current += timedelta(days=1)

    return trading_days


class YearClock:
    def __init__(self, trading_days):
        self.trading_days = trading_days
        self.index = 0

    def get_current_time(self):
        return self.trading_days[self.index]

    def increase(self):
        self.index += 1
        if self.index >= len(self.trading_days):
            self.index = len(self.trading_days) - 1  # capped fallback
