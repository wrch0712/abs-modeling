
class Asset(object):
    """
    Asset class contains various types of asset
    attributes: initial value
    methods: calculate monthly depreciation rate and current value
    """

    def __init__(self, valueInitial):  # initialization
        self._valueInitial = valueInitial

    # return initial value
    @property
    def valueInitial(self):
        return self._valueInitial

    # return a yearly depreciation rate
    def yearlyDeprRate(self):
        return 0.1

    # calculate the monthly depreciation rate
    def monthlyDeprRate(self):
        return self.yearlyDeprRate()/12

    # current value of the asset, for a given period
    def valueCurrent(self, period):
        return self._valueInitial * (1 - self.monthlyDeprRate()) ** period
