from DBConnector import DBConnector
from datetime import datetime, timedelta
import plotly.graph_objects as go

class Month:
    def __init__(self, ID, name, URL):
        self.prices = []
        self.times = []
        self.name = name
        self.URL = URL + "1m"
        self.Aktie_ID = ID
        self.slope = 0
        self.trading_days = get_last_trading_days()
        self.percent_change = None
        self.r_squared = None

    def GetMonth(self, tradeRepublic):
        self.prices = tradeRepublic.GetDataFromURI(self.URL)
        self.trading_days = get_last_trading_days()
        self.times = self.generate_month_times(len(self.prices))

    def generate_month_times(self, n):
        times = []
        clock = MonthClock(self.trading_days)
        for _ in range(n):
            times.append(clock.get_current_time())
            clock.increase()
        return times

    def GetMonthFromDB(self, aktie_id, data):
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

    def DrawMonth(self):
        if len(self.prices) != len(self.times):
            print("Unterschiedliche Länge von Preisen und Zeiten")
            return

        x = [self.time_to_minutes(t) for t in self.times]
        m, b = self.GetSlopeForDraw()
        regression_line = [m * xi + b for xi in x]
        x_labels = [t.strftime("%d.%m. %H:%M") for t in self.times]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_labels, y=self.prices, mode='lines+markers', name='Preise'))
        fig.add_trace(go.Scatter(x=x_labels, y=regression_line, mode='lines', name='Regression', line=dict(color='red')))

        fig.update_layout(title=f"Preisentwicklung (Monat) – {self.name}",
                          xaxis_title="Zeit",
                          yaxis_title="Preis (€)",
                          template="plotly_dark")
        fig.show()

    def PushData(self):
        if len(self.prices) == len(self.times):
            connector = DBConnector()
            connector.Startconnection()
            connector.PushMonth(self)  # kann angepasst werden auf PushMonth()
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

    try:
        last_month = today.replace(month=today.month - 1)
    except ValueError:
        # Sonderfall Januar → Dezember des Vorjahres
        last_month = today.replace(year=today.year - 1, month=12)

    start_date = last_month
    trading_days = []
    current = start_date

    while current <= today:
        if current.weekday() < 5:
            trading_days.append(current.replace(hour=0, minute=0, second=0, microsecond=0))
        current += timedelta(days=1)

    return trading_days




class MonthClock:
    def __init__(self, trading_days):
        self.trading_days = trading_days
        self.day_index = 0
        self.hour_index = 0
        self.hours = [6, 10, 14, 18, 22]

    def get_current_time(self):
        return self.trading_days[self.day_index].replace(hour=self.hours[self.hour_index])

    def increase(self):
        self.hour_index += 1
        if self.hour_index >= len(self.hours):
            self.hour_index = 0
            self.day_index += 1
            if self.day_index >= len(self.trading_days):
                self.day_index = len(self.trading_days) - 1  # capped fallback