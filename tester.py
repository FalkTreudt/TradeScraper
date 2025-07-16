from Clock import Clock

testclock = Clock()


for i in range(4):
    testclock.increaseMinutes(10)
print(testclock.GetTime())