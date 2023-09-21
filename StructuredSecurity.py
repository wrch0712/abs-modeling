
from StandardTranche import StandardTranche


class StructuredSecurity(object):
    """
    StructuredSecurity class contains and operates on a pool of standard tranches
    attributes: mode('Sequential' or 'Pro Rata'), some standard tranches from standardTranche class
    methods: add tranches to a StructuredSecurity object, flag mode('Sequential' or 'Pro Rata' ),
    increases the current time period for each tranche, make payments, get waterfall on liability side
    """

    def __init__(self, mode, *args):
        if mode == 'Sequential' or mode == 'Pro Rata':
            self.mode = mode
        else:
            raise Exception('approach should be "Sequential" or "Pro Rata"')

        for tranche in args:
            if isinstance(tranche, StandardTranche):  # check input tranches are from class StandardTranche
                self.args = list(args)
            else:
                raise Exception('input should be objects from StandardTranche')

        # sorted tranches by subordination
        self.args = sorted(self.args, key=lambda x: x.subordination)

        # initialized with a total Notional amount
        self.totalNotionalAmount = sum([tranche.notional for tranche in self.args])
        for tranche in args:
            tranche.principalDue = {}
            tranche.principalShortfall = 0
        self.balanceDict = {}  # key: period, value: dict(key: tranche number, value: balance of the tranche)
        self.cashLeft = 0

    def addTranche(self, *args):
        # instantiate and add the tranche to the StructuredSecurity object’s internal list of tranches
        for tranche in args:
            if isinstance(tranche, StandardTranche):  # check input tranches are from class StandardTranche
                self.args += self.addTranche(list(args))
            else:
                raise Exception('tranches added should be objects from StandardTranche')
        # sorted tranches by subordination
        self.args = sorted(self.args, key=lambda x: x.subordination)

    # Add a method that can change flags ‘Sequential’ or ‘Pro Rata’ modes on the object
    def approach(self, mode):
        if mode == 'Sequential' or mode == 'Pro Rata':
            return self.mode
        else:
            raise Exception('approach should be "Sequential" or "Pro Rata"')

    # Add a method that increases the current time period for each tranche.
    def increasePeriod(self):
        # # delegate to function in StandardTranche class to increases the current time period for each tranche
        for tranche in self.args:
            tranche.increaseTimePeriod()
            self.balanceDict[tranche.period] = {}

    def makePayments(self, cash_amount, principalCollection):
        # add cash left from previous period
        cash_amount += self.cashLeft

        # first pay interest
        for tranche in self.args:
            tranche.interestDueFunc()  # Ask each tranche for its interest due
            if cash_amount >= 0:
                tranche.makeInterestPayment(min(cash_amount, tranche.interestDue[tranche.period]))
                cash_amount -= min(cash_amount, tranche.interestDue[tranche.period])
            else:
                # If there is not enough cash to pay the interest in either tranche (a ‘shortfall’),
                # it gets added onto the interest owed in the next period (in the method of class StandardTranche)
                tranche.makeInterestPayment(0)

        # pay principal payment
        # if mode flag is 'Sequential
        if self.mode == 'Sequential':
            for num, tranche in enumerate(self.args):
                if num == 0 or self.balanceDict[tranche.period][num-1] == 0:
                    # if it's the first tranche or the prior tranche's principal has already been paid off,
                    # it will go to pay next tranche's principal

                    # calculate principal due: min(principal received + prior principal shortfalls, balance)
                    tranche.principalDue[tranche.period] = min(principalCollection + tranche.principalShortfall,
                                                               tranche.notionalBalance[tranche.period-1])
                else:
                    # the prior tranche's principal has not been paid off, the principal due is 0
                    tranche.principalDue[tranche.period] = 0

                if cash_amount > 0:
                    tranche.makePrincipalPayment(min(cash_amount, tranche.principalDue[tranche.period]))
                    cash_amount -= min(cash_amount, tranche.principalDue[tranche.period])
                    tranche.principalShortfall += tranche.principalDue[tranche.period] - \
                                                       min(cash_amount, tranche.principalDue[tranche.period])
                else:
                    # If there is not enough cash to pay the interest in either tranche (a ‘shortfall’),
                    # it gets added onto the interest owed in the next period (in the method of class StandardTranche)
                    tranche.makePrincipalPayment(0)
                    tranche.principalShortfall += tranche.principalDue[tranche.period]

                tranche.notionalBalanceFunc()  # Ask tranche for its balance
                self.balanceDict[tranche.period][num] = tranche.notionalBalance[tranche.period]

        # if mode flag is 'Pro Rata'
        if self.mode == 'Pro Rata':
            for tranche in self.args:
                # calculate principal due: min(principal received*tranche% + prior principal shortfalls, balance)
                tranche.principalDue[tranche.period] = min(principalCollection*tranche.notional/self.totalNotionalAmount
                                                           + tranche.principalShortfall,
                                                           tranche.notionalBalance[tranche.period-1])
                if cash_amount > 0:
                    tranche.makePrincipalPayment(min(cash_amount, tranche.principalDue[tranche.period]))
                    cash_amount -= min(cash_amount, tranche.principalDue[tranche.period])
                    tranche.principalShortfall += tranche.principalDue[tranche.period] - \
                                                   min(cash_amount, tranche.principalDue[tranche.period])
                else:
                    # If there is not enough cash to pay the interest in either tranche (a ‘shortfall’),
                    # it gets added onto the interest owed in the next period (in the method of class StandardTranche)
                    tranche.makePrincipalPayment(0)
                    tranche.principalShortfall += tranche.principalDue[tranche.period]
                tranche.notionalBalanceFunc()  # Ask each tranche for its balance

        # store cash left
        self.cashLeft = max(cash_amount, 0)

    # get a list of lists, each inner list represents a tranche, and contains the following values
    # for a given time period: Interest Due, Interest Paid, Interest Shortfall, Principal Paid, Balance.
    def getWaterfall(self):
        l = []
        for tranche in self.args:
            l.append([tranche.interestDue[tranche.period], tranche.interestPayment[tranche.period],
                      tranche.interestShortfall[tranche.period], tranche.principalPayment[tranche.period],
                      tranche.notionalBalance[tranche.period]])
        return l, self.cashLeft
