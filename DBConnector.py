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
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')

        for i in range(len(Day.prices)):
            #print(f"INSERT INTO Preise VALUES ({Day.Aktie_ID}, '{Day.prices[i]}','{formatted_date}','{Day.times[i]}')")
            self.cursor.execute(f"INSERT INTO Preise VALUES ('{Day.Aktie_ID}', '{Day.times[i]}','{formatted_date}','{Day.prices[i]}')")
            self.connection.commit()

    def GetPricesByID(self,ID):
        self.cursor.execute(f"SELECT * FROM Preise WHERE Aktie_ID = {ID}")
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    def GetNewID(self):
        self.cursor.execute("SELECT MAX(Aktie_ID) FROM Aktien")
        result = self.cursor.fetchall()
        for row in result:
            print(f"Neue ID = {row[0]}")

    def closeConnection(self):
        self.connection.close()
