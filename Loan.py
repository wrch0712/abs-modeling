
from Asset import Asset


class Loan(object):
    """
    Loan class contains various types of loans
    attributes : asset(object from asset class), term, rate, face
    methods: check if the loan default, calculate monthly payment, total payment, total interest,
    interest due, principal due, balance of a given period.
    """

    def __init__(self, asset, term, rate, face):  # initialization function
        if term > 0 and isinstance(term, int):
            self._term = term
        else:
            raise Exception('term should a positive integer')

        self._rate = rate

        if face > 0:
            self._face = face
        else:
            raise Exception('face should be positive')

        if isinstance(asset, Asset):  # if asset is an object derived from Asset class
            self._asset = asset
        else:
            raise Exception('parameter asset should be an object from class Asset')

        self.default = 1

    @property  # getter property method
    def term(self):
        return self._term

    @property  # getter property method
    def rate(self):
        return self._rate

    @property  # getter property method
    def face(self):
        return self._face

    @term.setter  # setter method
    def term(self, term):
        self._term = term

    @rate.setter  # setter method
    def rate(self, rate):
        self._rate = rate

    @face.setter  # setter method
    def face(self, face):
        self._face = face

    # determines whether or not the loan defaults for a given time period
    def checkDefault(self, number):
        if number == 0:  # if the loan default
            self.default = 0  # flags the loan as defaulted (return 0) if the passed-in number is 0
        else:
            self.default = 1
        return self.default

    def monthlyPayment(self, period=None):
        pmt = self.rate / 12 * self.face / (1 - (1 + self.rate / 12) ** (-self.term))  # use formula of loan
        return pmt

    def totalPayments(self, period=None):
        tp = self.monthlyPayment(period=None) * self.term
        return tp

    def totalInterest(self, period=None):
        ti = self.totalPayments() - self.face
        return ti

    # version that uses the formulas provided
    def interestDueFormulas(self, period):
        if self.default == 0:
            interest_due = 0  # If the loan is defaulted, the interest becomes 0
        else:
            if 0 <= period <= self.term:
                interest_due = self.balanceFormulas(period - 1) * self.rate / 12
            else:
                interest_due = 0
        return interest_due

    def principalDueFormulas(self, period):
        if self.default == 0:
            principal_due = 0  # If the loan is defaulted, the principal becomes 0
        else:
            if 0 <= period <= self.term:
                principal_due = self.monthlyPayment() - self.interestDueFormulas(period)
            else:
                principal_due = 0
        return principal_due

    def balanceFormulas(self, period):
        if self.default == 0:
            bal = 0  # If the loan is defaulted, the balance becomes 0
        else:
            if 0 <= period <= self.term:
                bal = self.face * (1 + self.rate / 12) ** period - self.monthlyPayment() * ((1 + self.rate / 12) ** period
                      - 1) / (self.rate / 12)  # use formula of loan
            else:
                bal = 0
        return bal

    def reset(self):
        self.default = 1
