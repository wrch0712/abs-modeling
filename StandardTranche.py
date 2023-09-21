
from Tranche import Tranche


class StandardTranche(Tranche):
    """
    StandardTranche class derives from Tranche class, it contains standard tranches
    it is initialized with notional, rate and a subordination flag
    Standard tranches start off with a certain notional and is able to keep track of all payments made to it.
    """

    def __init__(self, notional, rate, subordination):
        super(StandardTranche, self).__init__(notional, rate, subordination)
        self.period = 0
        self.principalPayment = {}
        self.interestPayment = {}
        self.notionalBalance = {0: self.notional}
        self.interestShortfall = {}
        self.sumInterestShortfall = {}
        self.interestDue = {}

    def increaseTimePeriod(self):
        # increase the current time period of the object by 1
        self.period += 1
        return self.period

    def makePrincipalPayment(self, pp):
        if self.principalPayment.get(self.period):
            # raise an error if it is called more than once for a given time period
            raise Exception('principal payment for this time period exists')
        elif self.notionalBalance == 0:
            # if the current notional balance is 0, the function should not accept the payment
            raise Exception('current notional balance is 0, no need for principle payment.')
        else:
            self.principalPayment[self.period] = pp
        return self.principalPayment

    def makeInterestPayment(self, ip):
        if self.interestPayment.get(self.period):
            # raise an error if it is called more than once for a given time period
            raise Exception('interest payment for this time period exists')
        elif self.interestDue == 0:
            # if the current interest due is 0, the function should not accept the payment
            raise Exception('no need for interest payment.')
        else:
            self.interestPayment[self.period] = ip

        # if the interest amount is less than the current interest due,
        # recorde the missing amount as an interest shortfall.
        self.interestShortfall[self.period] = max(self.interestDue[self.period] - ip, 0)

        return self.interestPayment, self.interestShortfall

    def notionalBalanceFunc(self):
        # calculate the sum of interest shortfall
        self.sumInterestShortfall[self.period] = sum([ish for period, ish in self.interestShortfall.items()
                                                     if period <= self.period])
        self.notionalBalance[self.period] = self.notionalBalance[self.period-1] - self.principalPayment[self.period] \
                                            + self.sumInterestShortfall[self.period]
        return self.notionalBalance

    def interestDueFunc(self):
        # calculate using the notional balance of the previous time period and the rate.
        # add interest shortfall from previous period.
        if self.period == 1:
            self.interestDue[self.period] = self.notional * self.rate / 12
        else:
            self.interestDue[self.period] = self.notionalBalance[self.period-1] * self.rate / 12 + self.interestShortfall[self.period-1]
        return self.interestDue

    def reset(self):
        self.period = 0
        self.principalPayment = {}
        self.interestPayment = {}
        self.notionalBalance = {0: self.notional}
        self.interestShortfall = {}
        self.sumInterestShortfall = {}
        self.interestDue = {}
