
from Tranche import Tranche


def doWaterfall(loanPool, structuredSecurity):
    """
    parameter: a LoanPool object and a StructuredSecurities object
    doWaterfall function will loop through time periods, starting from 0, and keep going until the LoanPool has no
    more active loans
    After the loop completes, the function will return all the results saved down from the getWaterfall function
    (on both asset side liabilities side)
    get a list of IRR of all tranches, a list of DIRR of all tranches, a list of AL of all tranches
    """

    # reset loans in loanPool and tranches in structuredSecurity
    for tranche in structuredSecurity.args:
        tranche.reset()
    for loan in loanPool.args:
        loan.reset()

    # get the maximum period until the LoanPool has no more active loans
    mp = max([loan.term for loan in loanPool.args])

    paymentDict = {}
    PrincipalPaymentDict = {}
    for num, tranche in enumerate(structuredSecurity.args):
        paymentDict[num] = []
        PrincipalPaymentDict[num] = []

    lwf = []
    swf = []
    cashLeft = []

    for i in range(1, mp+1):
        # call checkDefaults on the LoanPool to check if loan in loan Pool default
        loanPool.checkDefaults(i)

        # Ask the LoanPool for its total payment for the current time period
        totalPayment = loanPool.totalPaymentDue(i)

        # Ask the LoanPool for its total principal payment for the current time period
        totalPrincipalPayment = loanPool.totalPrincipalDue(i)

        # Increase the time period on the StructuredSecurities object
        structuredSecurity.increasePeriod()

        # Pay the StructuredSecurities with the amount provided by the LoanPool.
        structuredSecurity.makePayments(totalPayment, totalPrincipalPayment)

        # Call getWaterfall on both the LoanPool and StructuredSecurities objects and save the info into two variables.
        lwf.append(loanPool.getWaterfall(i))
        z = structuredSecurity.getWaterfall()[0]
        swf.append(structuredSecurity.getWaterfall()[0])
        cashLeft.append(structuredSecurity.getWaterfall()[1])

        for num, tranche in enumerate(z):
            # get payment (sum of interest payment and principal payment) of peroid i
            paymentDict[num].append(tranche[1]+tranche[3])
            # get principal payment of period i
            PrincipalPaymentDict[num].append(tranche[3])

    # calculate IRR and DIRR
    # get list of total payment (it's a list of list, the inner list show payment of all period of a tranche)
    paymentList = list(paymentDict.values())
    # get list of notional
    notionalList = [tranche.notional for tranche in structuredSecurity.args]
    # get list of tranche rate
    rateList = [tranche.rate for tranche in structuredSecurity.args]
    # calculate IRR using method in Tranche Class, it will return a list of IRR of all tranches
    # calculate DIRR using method in Tranche Class, it will return a list of DIRR of all tranches
    irrList = []
    dirrList = []
    for num, payment in enumerate(paymentList):
        irrList.append(Tranche.irr(notionalList[num], paymentList[num]))
        dirrList.append(Tranche.dirr(rateList[num], notionalList[num], paymentList[num]))

    # calculate AL
    # get list of principal payment
    # (it's a list of list, the inner list show principal payment of all period of a tranche)
    principalPaymentList = list(PrincipalPaymentDict.values())
    # calculate AL using method in Tranche Class, it will return a list of AL of all tranches
    alList = []
    for num, principalPayment in enumerate(principalPaymentList):
        alList.append(Tranche.al(notionalList[num], principalPaymentList[num]))

    return lwf, swf, cashLeft, irrList, dirrList, alList
