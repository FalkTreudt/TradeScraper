class Clock:
    def __init__(self,hour,min):
        self.min = min
        self.hours = hour
        self.day = 0

    def increaseMinutes(self,min):
        if(self.min != 50):
            self.min += min
        else:
            self.min = 0
            self.hours += 1
    def increaseHour(self):
        if self.hours != 23:
            self.hours += 1
        else:
            self.hours = 0
            self.day += 1

    def GetTime(self):
        if self.min != 0:
            return (f"{self.hours}:{self.min}")
        else:
            return (f"{self.hours}:00")
    def GetWeekTime(self):
            return (f"{self.day}:{self.hours}:{self.min}")