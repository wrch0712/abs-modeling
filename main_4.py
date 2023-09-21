"""
main 4: test runMonteParallel with multiprocessing
"""

from Asset import Asset
from Loan import Loan
from LoanPool import LoanPool
from StandardTranche import StandardTranche
from StructuredSecurity import StructuredSecurity
from runMonteParallel import runMonteParallel
import random
import multiprocessing


def main():
    print('\nRuochen Wang'
          '\nmain 4: test runMonteParallel with multiprocessing')

    multiprocessing.freeze_support()
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
    ta = StandardTranche(15000000, 0.05, 1)
    tb = StandardTranche(lp.totalPrincipal() - 15000000, 0.08, 2)
    ss = StructuredSecurity('Sequential', ta, tb)

    # let tolerance be 0.005, try 200 simulations and 5 processes
    rm = runMonteParallel(lp, ss, 0.005, 200, 5)

    # get DIRR
    print('\nDIRR of standard tranche "ta":', rm[0])
    print('DIRR of standard tranche "tb":', rm[1])

    # get AL
    print('\nAL of standard tranche "ta":', rm[2])
    print('AL of standard tranche "tb":', rm[3])

    # get rate
    print('\nrate of standard tranche "ta":', rm[4])
    print('rate of standard tranche "tb":', rm[5])

    # get rating
    print('\nDIRR of standard tranche "ta" is 0, the rating of "ta" is Aaa.'
          '\nDIRR of standard tranche "tb" is 0, the rating of "tb" is Aaa.')


if __name__ == '__main__':
    main()
