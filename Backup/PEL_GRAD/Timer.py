import time

class Timer():
    def __init__(self):
        self.t = list()
        self.t.append(['Big Bang', time.time()])

    def flag(self, name = '', show = False):
        self.t.append([name, round((time.time() - 
                                    self.t[0][1]) * 1000, 2)])
        if show:
            print(name, self.t[-1][1], "ms")

    def table(self):
        for i in range(1,len(self.t)):
            print(self.t[i])