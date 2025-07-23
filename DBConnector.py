# ---------- DBConnector.py ----------
from datetime import datetime, timedelta
import mysql.connector
from Utils import get_last_5_trading_days

class DBConnector:
    def __init__(self):
        self.IP = '192.168.178.47'
        self.port = 3306
        self.user = 'admin'
        self.pw = 'falk'
        self.database = 'TradeScraper'
        self.product_id_cache = {}

    def Startconnection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.IP,
                port=self.port,
                user=self.user,
                password=self.pw,
                database=self.database
            )
            if self.connection.is_connected():
                print('Verbindung zur Datenbank erfolgreich')
                self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Fehler bei der Verbindung: {err}")
            raise

    def closeConnection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Datenbankverbindung geschlossen.")



    def PushDay(self,Day):
        print('Lade Daten hoch')
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')
        try:
            for i in range(len(Day.prices)):
                self.cursor.execute(f"INSERT INTO Preise VALUES ('{Day.Aktie_ID}', '{Day.times[i]}','{formatted_date}','{Day.prices[i]}')")
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Fehler beim Hochladen der Daten: {err}")

    def PushWeek(self, Week):
        print('Lade Wochendaten hoch')
        current_date = datetime.now().strftime('%Y-%m-%d')
        try:
            for i in range(len(Week.prices)):
                zeit = Week.times[i]

                # Zeit als datetime interpretieren, falls notwendig
                if isinstance(zeit, str):
                    zeit = self.parse_week_time(zeit)
                if not isinstance(zeit, datetime):
                    continue  # überspringen, wenn nicht interpretierbar

                # Handelszeiten: nur zwischen 07:00 und 21:59 Uhr
                if 7 <= zeit.hour <= 22:
                    zeit_str = zeit.strftime('%Y-%m-%d %H:%M:%S')
                    self.cursor.execute(
                        "INSERT INTO PreiseWoche (Aktie_ID, zeit, datum, preis) VALUES (%s, %s, %s, %s)",
                        (Week.Aktie_ID, zeit_str, current_date, Week.prices[i])
                    )
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Fehler beim Hochladen der Wochendaten: {err}")

    def GetProducts(self):
        print('Start getting URLs')
        try:
            self.cursor.execute("SELECT Aktie_ID, Name, URL FROM Aktien")
            result = self.cursor.fetchall()
            IDs, names, urls = zip(*result) if result else ([], [], [])
            return [list(IDs), list(names), list(urls)]
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Produkte: {err}")
            return [[], [], []]

    def GetCurrentDays(self):
        try:
            self.cursor.execute("SELECT Aktie_ID, preis, zeit FROM Preise")
            result = self.cursor.fetchall()

            data = {}
            for aktie_id, preis, zeit in result:
                if aktie_id not in data:
                    data[aktie_id] = {"preise": [], "zeiten": []}
                data[aktie_id]["preise"].append(preis)
                data[aktie_id]["zeiten"].append(zeit)

            return data
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Tagesdaten: {err}")
            return {}

    def GetCurrentWeek(self):
        try:
            self.cursor.execute("SELECT Aktie_ID, preis, zeit FROM PreiseWoche")
            result = self.cursor.fetchall()

            data = {}
            for aktie_id, preis, zeit_str in result:
                if aktie_id not in data:
                    data[aktie_id] = {"preise": [], "zeiten": []}
                zeit = self.parse_week_time(zeit_str)
                if zeit:
                    data[aktie_id]["preise"].append(preis)
                    data[aktie_id]["zeiten"].append(zeit)

            return data
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Wochen-Daten: {err}")
            return {}

    def parse_week_time(self, zeit_str):
        from datetime import datetime, timedelta
        try:
            if isinstance(zeit_str, datetime):
                return zeit_str  # schon als datetime-Objekt
            if ":" in zeit_str and zeit_str.count(":") == 2 and "-" in zeit_str:
                # Format: "2025-07-22 06:00:00"
                return datetime.strptime(zeit_str, "%Y-%m-%d %H:%M:%S")
            elif ":" in zeit_str and zeit_str.count(":") == 2:
                # Format: "0:9:00" → eigener Zeitindex
                day, hour, minute = map(int, zeit_str.split(":"))
                last_5_days = get_last_5_trading_days()
                if day < len(last_5_days):
                    base_date = last_5_days[day].replace(hour=0, minute=0, second=0, microsecond=0)
                    return base_date + timedelta(hours=hour, minutes=minute)
            else:
                print(f"Unbekanntes Zeitformat: {zeit_str}")
                return None
        except Exception as e:
            print(f"Fehler beim Parsen der Zeit '{zeit_str}': {e}")
            return None

    def PushMonth(self, month_obj):
        print('Lade Monatsdaten hoch')
        current_date = datetime.now().strftime('%Y-%m-%d')
        try:
            for i in range(len(month_obj.prices)):
                self.cursor.execute(
                    "INSERT INTO PreiseMonat (Aktie_ID, zeit, datum, preis) VALUES (%s, %s, %s, %s)",
                    (month_obj.Aktie_ID, month_obj.times[i], current_date, month_obj.prices[i])
                )
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Fehler beim Hochladen der Monatsdaten: {err}")

    def GetCurrentMonth(self):
        try:
            self.cursor.execute("SELECT Aktie_ID, preis, zeit FROM PreiseMonat")
            result = self.cursor.fetchall()

            data = {}
            for aktie_id, preis, zeit in result:
                if aktie_id not in data:
                    data[aktie_id] = {"preise": [], "zeiten": []}
                data[aktie_id]["preise"].append(preis)
                data[aktie_id]["zeiten"].append(zeit)

            return data
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Monatsdaten: {err}")
            return {}

    def PushYear(self, Year):
        print('Lade Jahresdaten hoch')
        current_date = datetime.now().strftime('%Y-%m-%d')
        try:
            for i in range(len(Year.prices)):
                self.cursor.execute(
                    "INSERT INTO PreiseJahr (Aktie_ID, zeit, datum, preis) VALUES (%s, %s, %s, %s)",
                    (Year.Aktie_ID, Year.times[i], current_date, Year.prices[i])
                )
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Fehler beim Hochladen der Monatsdaten: {err}")

    def GetCurrentYear(self):
        try:
            self.cursor.execute("SELECT Aktie_ID, preis, zeit FROM PreiseJahr")
            result = self.cursor.fetchall()

            data = {}
            for aktie_id, preis, zeit in result:
                if aktie_id not in data:
                    data[aktie_id] = {"preise": [], "zeiten": []}
                data[aktie_id]["preise"].append(preis)
                data[aktie_id]["zeiten"].append(zeit)

            return data
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der JahresDaten: {err}")
            return {}

