
import random


class LoanPool(object):
    """
    LoanPool class contains and operates on a pool of loans (composition)
    attributes: some loans from Loan class
    methods: return total loan principal, total loan balance for a given period, aggregate principal, interest,
    and total payment due in a given period, number of ‘active’ loans, Weighted Average Maturity (WAM) and
    Weighted Average Rate (WAR) of the loans.
    get waterfall of loans in loanPool
    check if loan in LoanPool defaults
    """

    def __init__(self, *args):
        self.args = args

    # get the total loan principal
    def totalPrincipal(self):
        sumPrincipal = 0
        for loan in self.args:
            sumPrincipal += loan.face  # delegate to function in Loan class to get face value
        return sumPrincipal

    # get the total loan balance for a given period
    def totalBalance(self, period):
        sumBalance = 0
        for loan in self.args:
            if loan.balanceFormulas(period) > 0:
                # delegate to function in Loan class to get loan balance for a given period
                sumBalance += loan.balanceFormulas(period)
        return sumBalance

    # get the aggregate principal, interest, and total payment due in a given period
    def totalPrincipalDue(self, period):
        sumPrincipalDue = 0
        for loan in self.args:
            sumPrincipalDue += loan.principalDueFormulas(period)
        return sumPrincipalDue

    def totalInterestDue(self, period):
        sumInterestDue = 0
        for loan in self.args:
            sumInterestDue += loan.interestDueFormulas(period)
        return sumInterestDue

    def totalPaymentDue(self, period):
        # total payment due in a given period is equal to principal due plus interest due in the given period
        return self.totalPrincipalDue(period)+self.totalInterestDue(period)

    # returns the number of 'active' loans
    def NumActiveLoan(self, period):
        activeLoan = 0
        for loan in self.args:
            if loan.balanceFormulas(period) > 0:
                activeLoan += 1
        return activeLoan

    # calculate the Weighted Average Maturity (WAM) and Weighted Average Rate (WAR) of the loans
    # Weighted Average Maturity (WAM)
    def wam(self):
        # get the list of amount
        amount = [loan.face for loan in self.args]  # delegate to function in Loan class
        # get the list of term multiple by amount
        term_multiple_amount = [loan.face * loan.term for loan in self.args]
        # calculate the weighted average rate
        wam = sum(term_multiple_amount) / sum(amount)
        return wam

    # Weighted Average Rate (WAR)
    def war(self):
        # get the list of amount
        amount = [loan.face for loan in self.args]  # delegate to function in Loan class
        # get the list of rate multiple by amount
        rate_multiple_amount = [loan.face * loan.rate for loan in self.args]
        # calculate the weighted average rate
        war = sum(rate_multiple_amount) / sum(amount)
        return war

    # get a list of lists, each inner list represents a loan, and contains the following values
    # for a given time period: Interest Due, Principal Paid, Balance.
    def getWaterfall(self, period):
        l = []
        for loan in self.args:
            l.append([loan.interestDueFormulas(period), loan.principalDueFormulas(period), loan.balanceFormulas(period)])
        return l

    # check if loan in LoanPool defaults
    def checkDefaults(self, period):
        for loan in self.args:
            if loan.default != 0:
                # if the loan hasn't defaulted before, check if it will default in this period
                if 1 <= period <= 10:
                    number = random.randint(0, 2000-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                elif 11 <= period <= 60:
                    number = random.randint(0, 1000-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                elif 61 <= period <= 120:
                    number = random.randint(0, 500-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                elif 121 <= period <= 180:
                    number = random.randint(0, 250-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                elif 181 <= period <= 210:
                    number = random.randint(0, 200-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                elif 211 <= period <= 360:
                    number = random.randint(0, 100-1)
                    loan.checkDefault(number)  # call checkDefault on Loan, passing in the random number
                else:
                    raise Exception('input period is too large')
