class Enterprise:
    def __init__(self, name='', rate=1, risk=[0]):
        self.name = name
        self.rate = rate
        self.risk = risk

    def mean_risk(self):
        return round(float(((sum(self.risk)/len(self.risk))**2)**0.5),4)

    def risk_lvl(self):
        if (self.mean_risk()<0.1):
            return 1
        if (self.mean_risk()<0.25):
            return 2
        return 3
