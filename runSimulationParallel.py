"""
runSimulationParallel function (using multiprocessing)
"""

import multiprocessing
from doWaterfall import doWaterfall


def doWork(input, output):
    while True:
        try:
            f, args = input.get(timeout=1)
            res = f(*args)
            output.put(res)
        except:
            output.put("Done")
            break


def runSimulationParallel(loanPool, structuredSecurit, NSIM, numProcesses):
    """
    parameter: a LoanPool object, a StructuredSecurities object, the number of simulations to run, number of Processes
    runSimulationParallel function call doWaterfall function NSIM number of times with multiprocessing
    and collect the resulting DIRR and AL from each iteration
    it return list of average DIRR of each tranche and list of average AL of each tranche
    """

    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # using do waterfall function, add NISM number of tuples to the input Queue
    for i in range(NSIM):
        input_queue.put((doWaterfall, (loanPool, structuredSecurit)))

    for i in range(numProcesses):
        p = multiprocessing.Process(target=doWork, args=(input_queue, output_queue))
        p.start()

    alldirrList = []
    allalList = []
    while True:
        r = output_queue.get()
        if r != 'Done':
            alldirrList.append(r[4])
            allalList.append(r[5])
        else:
            break

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
