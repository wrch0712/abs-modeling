
import numpy_financial
from functools import reduce


class Tranche(object):
    """
    Tranche Class contains various types of tranches
    it is initialized with notional, rate and a subordination flag
    methods: calculate IRR, DIRR, AL
    """

    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination

    @property  # getter property method
    def notional(self):
        return self._notional

    @property  # getter property method
    def rate(self):
        return self._rate

    @property  # getter property method
    def subordination(self):
        return self._subordination

    @notional.setter  # setter method
    def notional(self, notional):
        self._notional = notional

    @rate.setter  # setter method
    def rate(self, rate):
        self._rate = rate

    @subordination.setter  # setter method
    def subordination(self, subordination):
        self._subordination = subordination

    # calculate Internal Rate of Return (IRR)
    @classmethod  # class-level methods
    def irr(cls, notional, payment):
        # calculate IRR using irr() function in numpy_financial and annualize it
        irr = numpy_financial.irr([-notional]+payment) * 12
        return irr

    # Reduction in Yield (DIRR)
    @classmethod  # class-level methods
    def dirr(cls, rate, notional, payment):
        # DIRR is the tranche rate less the annual IRR
        return rate - Tranche.irr(notional, payment)

    # calculate Average Life (AL)
    @classmethod  # class-level methods
    def al(cls, initialPrincipal, principalPayment):
        if principalPayment[-1] == 0:
            # If the loan was paid down (balance = 0), AL can be calculated
            # AL is the inner product of the time period numbers and the principal payments
            # divided by the initial principal
            periodMultiplyPrincipalPayment = reduce(lambda total, x: total+(x[0]+1)*x[1],
                                                    enumerate(principalPayment), 0)
            return periodMultiplyPrincipalPayment / initialPrincipal
        else:
            # If the loan was not paid down (balance != 0), then AL is infinite
            return None
