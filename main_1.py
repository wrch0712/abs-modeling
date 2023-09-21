"""
main 1: test doWaterFall with loan default
"""

from Asset import Asset
from Loan import Loan
from LoanPool import LoanPool
from StandardTranche import StandardTranche
from StructuredSecurity import StructuredSecurity
from doWaterfall import doWaterfall
import csv
import random


def main():
    print('\nRuochen Wang'
          '\nmain 1: test doWaterFall with loan default')

    random.seed(73)  # set seed

    # Create a LoanPool object that consists of 1,500 loans.
    with open('/Users/wrc/Desktop/python HW/Ruochen Wang_ABS modeling/Loans_data.csv', 'r',) as f:
        next(f)  # skip header line
        loan = []
        for line in f:
            l = line.rstrip("', '', '', '', '\n'").split(',')  # convert lines of csv into list
            loan.append(Loan(Asset(float(l[6])), int(l[4]), float(l[3]), float(l[2])))
    lp = LoanPool(*loan)

    # Instantiate StructuredSecurity object
    # add two standard tranches
    ta = StandardTranche(15000000, 0.02, 1)
    tb = StandardTranche(lp.totalPrincipal()-15000000, 0.04, 2)
    ss = StructuredSecurity('Sequential', ta, tb)

    # Call doWaterfall and save the results into two CSV files
    dwf = doWaterfall(lp, ss)
    loanWf = dwf[0]
    trancheWf = dwf[1]
    cashLeft = dwf[2]

    # save CSV files for the asset side
    l1 = []
    for period in loanWf:
        l1.append([i for loan in period for i in loan])
    with open('waterfallAsset.csv', 'w') as fl:
        wl = csv.writer(fl)
        wl.writerow(['InterestDue', 'PrincipalDue', 'Balance']*1500)  # add header
        wl.writerows(l1)

    # save CSV files for the liability side
    t1 = []
    for period in trancheWf:
        t1.append([i for tranche in period for i in tranche] + [' ', cashLeft[trancheWf.index(period)]])
    with open('waterfallLiability.csv', 'w') as ft:
        wt = csv.writer(ft)
        wt.writerow(['InterestDue', 'InterestPaid', 'Interest Shortfall', 'Principal Paid', 'Balance', 'InterestDue',
                     'InterestPaid', 'Interest Shortfall', 'Principal Paid', 'Balance', ' ', 'Cash Left'])  # add header
        wt.writerows(t1)

    print('\ntwo CSV files (one for the asset side and one for the liabilities side) created successfully.')

    # get IRR
    print('\nIRR of standard tranche "ta":', dwf[3][0])
    print('IRR of standard tranche "tb":', dwf[3][1])

    # get DIRR
    print('\nDIRR of standard tranche "ta":', dwf[4][0])
    print('DIRR of standard tranche "tb":', dwf[4][1])

    # get AL
    print('\nAL of standard tranche "ta":', dwf[5][0])
    print('AL of standard tranche "tb":', dwf[5][1])

    # get letter rate
    print('\nIn this case, some loans default.'
          '\nDIRR of standard tranche "ta" is still 0, rating of "ta" is Aaa.'
          '\nDIRR of standard tranche "tb" becomes 0.8166% and AL of "tb" becomes infinite, '
          'rating of "tb" becomes Ba2.')


if __name__ == '__main__':
    main()
