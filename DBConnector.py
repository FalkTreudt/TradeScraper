from TradeRepublic import TradeRepublic
import mysql.connector
from datetime import datetime

class DBConnector:
    def __init__(self):
        self.IP = '192.168.178.47'
        self.port = 3306
        self.user = 'admin'
        self.pw = 'falk'
        self.database = 'TradeScraper'

        self.days = []

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
            raise  # Fehlermeldung werfen, wenn die Verbindung fehlschlägt


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

    def GetPricesByID(self,ID):
        print(f'Start loading prices of ID {ID}')
        try:
            self.cursor.execute(f"SELECT * FROM Preise WHERE Aktie_ID = {ID}")
            result = self.cursor.fetchall()
            for row in result:
               print(row)
        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Daten von ID {ID}: {err}")
    def GetCurrentDataFromID(self,ID):
        try:
            self.cursor.execute(f"SELECT preis, zeit FROM Preise WHERE Aktie_ID = {ID}")
            result = self.cursor.fetchall()
            prices = []
            times = []
            for row in result:
                prices.append(row[0])
                times.append(row[1])

            return [prices,times]

        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Daten von ID {ID}: {err}")

    def GetCurrentDays(self):
        try:
            ids_str = ",".join(str(i) for i in range(self.GetNumberOfProducts()))
            self.cursor.execute(f"SELECT Aktie_ID, preis, zeit FROM Preise WHERE Aktie_ID IN ({ids_str})")
            result = self.cursor.fetchall()

        # Dictionary für Zuordnung von ID -> [preise], [zeiten]
            data = {}
            for aktie_id, preis, zeit in result:
             if aktie_id not in data:
                    data[aktie_id] = {"preise": [], "zeiten": []}
             data[aktie_id]["preise"].append(preis)
             data[aktie_id]["zeiten"].append(zeit)
            self.dayData = data
            print(f'Data an stelle 52: {data[52]}')
            return data  # Dictionary mit allen Daten

        except mysql.connector.Error as err:
            print(f"Fehler beim Laden der Daten von ID : {err}")
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

    def CheckEntry(self,name):
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


    def PushProducts(self,names,urls):
        print('Start pushing Products')
        if len(names) == len(urls):
            try:
                for i in range(len(names)):
                    self.CreateEntry(names[i],urls[i])
            except mysql.connector.Error as err:
                print(f"Fehler beim Pushen der Aktien: {err}")


    def GetProducts(self):
        print('Start getting URLS')
        try:
            self.cursor.execute("SELECT Aktie_ID,Name,URL FROM Aktien")
            result = self.cursor.fetchall()
            urls = []
            names = []
            IDs = []
            for row in result:
                IDs.append(row[0])
                names.append(row[1])
                urls.append(row[2])

            data = [IDs,names,urls]
            return data
        except mysql.connector.Error as err:
            print(f"Fehler beim Checken der ID: {err}")
    def GetProductID(self,name):
        print('Start getting Product_ID')
        try:
            self.cursor.execute(f"SELECT Aktie_ID FROM Aktien WHERE name= '{name}'")
            result = self.cursor.fetchall()
            name = ''
            for row in result:
                name = row[0]
            return name
        except mysql.connector.Error as err:
            print(f"Fehler beim holen der ID mit dem Namen {name}: {err}")
    def GetNumberOfProducts(self):
        print('Start getting Number of Products')
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Aktien")
            result = self.cursor.fetchall()
            count = result[0][0]
            return int(count)
        except mysql.connector.Error as err:
            print(f"Fehler beim Checken der ID: {err}")

    def closeConnection(self):
        self.connection.close()

