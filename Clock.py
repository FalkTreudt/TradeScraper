class Clock:
    def __init__(self):
        self.min = 30
        self.hours = 7

    def increaseMinutes(self,min):
        if(self.min != 50):
            self.min += min
        else:
            self.min = 0
            self.hours += 1

    def GetTime(self):
        if self.min != 0:
            return (f"{self.hours}:{self.min}")
        else:
            return (f"{self.hours}:00")