from Clock import Clock
from DBConnector import DBConnector

connector = DBConnector()
connector.Startconnection()
#connector.PushDay()
connector.GetNewID()

connector.closeConnection()