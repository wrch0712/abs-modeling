"""
runMonte function without multiprocessing (using simulateWaterfall)
"""

from simulateWaterfall import simulateWaterfall
import math


def calculateYield(a, d):
    y = (7/(1+0.08*math.exp(-0.19*a/12))+0.019*math.sqrt(a/12*abs(d)*100))/100
    return y


def runMonte(loanPool, structuredSecurit, tolerance, NSIM):
    """
    parameter: a LoanPool object, a StructuredSecurities object, tolerance, the number of simulations to run
    runMonte function loop through simulateWaterfall and adjust the tranche rates to reflect the yields
    it returns DIRR, WAL, and rate of each tranche
    """

    # get tranche notional
    TrancheNotional = [tranche.notional for tranche in structuredSecurit.args]
    TrancheNotionalA = TrancheNotional[0]
    TrancheNotionalB = TrancheNotional[1]

    # Initialize difference(make it greater than tolerance) to start the first while loop
    diff = tolerance + 0.1
    irra = None
    irrb = None
    ala = None
    alb = None
    ya = None
    yb = None

    while diff >= tolerance:
        # Invoke the simulateWaterfall
        swf = simulateWaterfall(loanPool, structuredSecurit, NSIM)

        if all(swf[1]):  # if AL for each tranche is finite

            # Save down the resulting average DIRR and AL for each tranche
            irra = swf[0][0]
            irrb = swf[0][1]
            ala = swf[1][0]
            alb = swf[1][1]

            # Call calculateYield function with the average DIRR and WAL for both tranches and save down the yields
            ya = calculateYield(ala, irra)
            yb = calculateYield(alb, irrb)

            # get initial tranche rate
            oldTrancheRate = [tranche.rate for tranche in structuredSecurit.args]
            oldTrancheRateA = oldTrancheRate[0]
            oldTrancheRateB = oldTrancheRate[1]

            # Calculate the new tranche rates
            coeff = oldTrancheRateA * 1.2 + oldTrancheRateB * 0.8
            newTrancheRateA = oldTrancheRateA + coeff * (ya - oldTrancheRateA)
            newTrancheRateB = oldTrancheRateB + coeff * (yb - oldTrancheRateB)

            # Calculate difference

            diff = (TrancheNotionalA * abs((oldTrancheRateA-newTrancheRateA)/oldTrancheRateA) +
                    TrancheNotionalB * abs((oldTrancheRateB-newTrancheRateB)/oldTrancheRateB))\
                   /(TrancheNotionalA+TrancheNotionalB)

            # modify the tranche rates to reflect the yields
            for num, tranche in enumerate(structuredSecurit.args):
                tranche.rate = [ya, yb][num]

        else:
            print('AL for certain tranche is infinite')
            break

    return irra, irrb, ala, alb, ya, yb
