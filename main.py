from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from TradeRepublic import TradeRepublic
from Day import Day
from Engine import Engine
from DBConnector import DBConnector





Engine1 = Engine(getDriver())
#Engine2 = Engine(getDriver())
Engine1.start()
#Engine2.start()
#Engine.PushProducts()
#Engine.CollectDayData()

#Engine.CollectWeekData()

#Engine.CollectMonthData()
Engine1.CollectYearData()
# Warten, um sicherzustellen, dass die Seite geladen wird
time.sleep(3000)


#time.sleep(30)

#driver.quit()
