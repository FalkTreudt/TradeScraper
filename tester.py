from Clock import Clock
from DBConnector import DBConnector

connector = DBConnector()
connector.Startconnection()
#connector.PushDay()
connector.CreateEntry("NVIDIA",'Grafikkarten')
print(connector.CheckEntry("Rheinmetall"))

connector.closeConnection()