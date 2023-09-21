"""
simulateWaterfall function (without multiprocessing)
"""

from doWaterfall import doWaterfall


def simulateWaterfall(loanPool, structuredSecurit, NSIM):
    """
    parameter: a LoanPool object, a StructuredSecurities object, the number of simulations to run
    simulateWaterfall function call doWaterfall function NSIM number of times
    and collect the resulting DIRR and AL from each iteration
    it return list of average DIRR of each tranche and list of average AL of each tranche
    """

    alldirrList = []
    allalList = []
    for i in range(int(NSIM)):
        dwf = doWaterfall(loanPool, structuredSecurit)
        alldirrList.append(dwf[4])
        allalList.append(dwf[5])

    # calculate average DIRR
    alldirrDict = {}  # a dict of DIRR (key: the number of tranche, value: a list of DIRR of each tranche)
    dirrAveList = []  # a list of average DIRR for all tranches
    for num, tranche in enumerate(structuredSecurit.args):
        alldirrDict[num] = [sublist[num] for sublist in alldirrList]
        # calculate average DIRR of the tranche
        dirrAveList.append(sum(alldirrDict[num])/len((alldirrDict[num])))

    # calculate average AL
    allalDict = {}  # a dict of AL (key: the number of tranche, value: a list of AL of each tranche)
    alAveList = []  # a list of average AL for all tranches
    for num, tranche in enumerate(structuredSecurit.args):
        allalDict[num] = [sublist[num] for sublist in allalList]
        if any(allalDict[num]):  # if values in allalDict[num] are not all None
            while None in allalDict[num]:  # remove None from AL values
                allalDict[num].remove(None)
            # calculate average AL of the tranche
            alAveList.append(sum(allalDict[num]) / len((allalDict[num])))
        else:
            alAveList.append(None)

    return dirrAveList, alAveList
