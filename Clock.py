import time

class Clock():
    def __init__(self):
        self.t = list()
        self.t.append(['Big Bang', time.time()])

    def flag(self, name = '', show = False, mode = "abs"):
        self.t.append([name, round((time.time() - 
                                    self.t[0][1]) * 1000, 2)])
        if show == True:
            if mode == "inc" and len(self.t) > 2:
                print(name, round(self.t[-1][1] -
                                self.t[-2][1], 2), "ms")
            else:
                print(name, self.t[-1][1], "ms")

    def table(self, mode = "abs"):
        if mode == "inc":
            print(self.t[1])
            for i in range(2,len(self.t)):
                print([self.t[i][0], round(self.t[i][1] - 
                                           self.t[i-1][1], 2)])
        else:
            for i in range(1,len(self.t)):
                print(self.t[i])


    def getPhaseTime(self, phase):
        return self.t[phase+1][1]
    
    def getAllTimes(self):
        d = {}
        d[self.t[1][0]] = self.t[1][1]
        for i in range(2,len(self.t)):
            d[self.t[i][0]] = round(self.t[i][1] - 
                                        self.t[i-1][1], 2)
            
        return d