"""
main 2: test simulateWaterfall
"""

from Asset import Asset
from Loan import Loan
from LoanPool import LoanPool
from StandardTranche import StandardTranche
from StructuredSecurity import StructuredSecurity
from simulateWaterfall import simulateWaterfall
import random


def main():
    print('\nRuochen Wang'
          '\nmain 2: test simulateWaterfall')

    random.seed(74)  # set seed

    # Create a LoanPool object that consists of 1,500 loans.
    with open('/Users/wrc/Desktop/python HW/Ruochen Wang_ABS modeling/Loans_data.csv', 'r', ) as f:
        next(f)  # skip header line
        loan = []
        for line in f:
            l = line.rstrip("', '', '', '', '\n'").split(',')  # convert lines of csv into list
            loan.append(Loan(Asset(float(l[6])), int(l[4]), float(l[3]), float(l[2])))
    lp = LoanPool(*loan)

    # Instantiate StructuredSecurity object
    # add two standard tranches
    ta = StandardTranche(15000000, 0.02, 1)
    tb = StandardTranche(lp.totalPrincipal() - 15000000, 0.04, 2)
    ss = StructuredSecurity('Sequential', ta, tb)

    # call simulateWaterfall function
    # try 200 simulations
    swf = simulateWaterfall(lp, ss, 200)

    # get DIRR
    print('\nDIRR of standard tranche "ta":', swf[0][0])
    print('DIRR of standard tranche "tb":', swf[0][1])

    # get AL
    print('\nAL of standard tranche "ta":', swf[1][0])
    print('AL of standard tranche "tb":', swf[1][1])

    print('\nDIRR of standard tranche "ta" is 0,rating of "ta" is Aaa.'
          '\nDIRR of standard tranche "tb" is 0.71% and AL of "tb" is infinite,'
          'rating of "tb" is Ba1.')


if __name__ == '__main__':
    main()
