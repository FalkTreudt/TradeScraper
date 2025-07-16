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

    def GetNewID(self):
        print('Start Check next ID')
        try:
            self.cursor.execute("SELECT MAX(Aktie_ID) FROM Aktien")
            result = self.cursor.fetchall()
            for row in result:
                print(f"Neue ID = {row[0]}")
                return row[0]
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

    def CreateEntry(self, name, category):
        try:
            if self.CheckEntry(name) == False:
                self.cursor.execute(
                    f"INSERT INTO Aktien VALUES ('{self.GetNewID() + 1}', '{name}','{category}','')")
                self.connection.commit()
                print(f"Eintrag für die Aktie {name} erstellt")
            else:
                print(f"Eintrag für die Aktie {name} bereits vorhanden!")
        except mysql.connector.Error as err:
            print(f"Fehler beim Erstellen der Aktie: {err}")


    def closeConnection(self):
        self.connection.close()
