# ---------- DBConnector.py ----------
from datetime import datetime, timedelta
import mysql.connector
from Utils import get_last_5_trading_days
import threading

class DBConnector:
    def __init__(self):
        self.IP = '192.168.178.97'
        self.port = 3307
        self.user = 'root'
        self.pw = '1234'
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
        self.Startconnection()
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

    def PushProducts(self, names, urls):
        print('Start pushing Products')
        if len(names) == len(urls):
            try:
                for i in range(len(names)):
                    self.CreateEntry(names[i], urls[i])
            except mysql.connector.Error as err:
                print(f"Fehler beim Pushen der Aktien: {err}")

    def GetNewID(self):
        print('Start Check next ID')
        try:
            self.cursor.execute("SELECT MAX(Aktie_ID) FROM Aktien")
            result = self.cursor.fetchall()
            for row in result:
                if row[0] != None:
                    return float(row[0])
                else:
                    return 0
        except mysql.connector.Error as err:
            print(f"Fehler beim Checken der ID: {err}")

    def CheckEntry(self, name):
        print(f'Start Checking for {name}')
        try:
            self.cursor.execute(f"SELECT * FROM Aktien WHERE name = '{name}'")
            result = self.cursor.fetchall()
            if len(result) == 0:
                return False
            else:
                return True
        except mysql.connector.Error as err:
            print(f"Fehler beim Checken der Aktie: {err}")
    def CreateEntry(self, name, URL):
        print(f'Start creating Entry for {name}')
        try:
            if self.CheckEntry(name) == False:
                self.cursor.execute(
                    f"INSERT INTO Aktien VALUES ('{self.GetNewID() + 1}', '{name}','{URL}','')")
                self.connection.commit()
                print(f"Eintrag für die Aktie {name} erstellt")
            else:
                print(f"Eintrag für die Aktie {name} bereits vorhanden!")
        except mysql.connector.Error as err:
            print(f"Fehler beim Erstellen der Aktie: {err}")

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

    def GetAllProductDataByName(self, name: str):
        """
        Holt Preis- und Zeitdaten für Day, Week, Month, Year anhand des Aktiennamens.

        Rückgabe:
            {
                "day":   {"preise": [...], "zeiten": [...]},
                "week":  {"preise": [...], "zeiten": [...]},
                "month": {"preise": [...], "zeiten": [...]},
                "year":  {"preise": [...], "zeiten": [...]}
            }
        """
        ids, names, urls = self.GetProducts()
        name_lower = name.lower()

        try:
            index = [n.lower() for n in names].index(name_lower)
            aktie_id = ids[index]
        except ValueError:
            print(f"❌ Aktie '{name}' nicht gefunden.")
            return {}

        result = {}

        for zeitraum, fetch_func in {
            "day": self.GetCurrentDays,
            "week": self.GetCurrentWeek,
            "month": self.GetCurrentMonth,
            "year": self.GetCurrentYear
        }.items():
            data = fetch_func()
            if aktie_id in data:
                preise = [float(p) for p in data[aktie_id]["preise"]]
                zeiten = data[aktie_id]["zeiten"]
                result[zeitraum] = {"preise": preise, "zeiten": zeiten}
            else:
                result[zeitraum] = {"preise": [], "zeiten": []}
                print(f"⚠️  Keine Daten für {zeitraum} bei ID {aktie_id}")

        return result

    def check_missing_ids_in_tables(self, ids):
        self.Startconnection()
        cursor = self.connection.cursor()

        id_set = set(ids)
        id_str = ','.join(str(i) for i in ids)
        tabellen = ["Preise", "PreiseWoche", "PreiseMonat", "PreiseJahr"]
        fehlende = {t: set() for t in tabellen}

        for tabelle in tabellen:
            query = f"""
                   SELECT DISTINCT Aktie_ID FROM {tabelle}
                   WHERE Aktie_ID IN ({id_str})
               """
            cursor.execute(query)
            vorhandene_ids = set(row[0] for row in cursor.fetchall())
            fehlende[tabelle] = id_set - vorhandene_ids

        cursor.close()
        return fehlende




