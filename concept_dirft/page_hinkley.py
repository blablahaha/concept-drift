"""Page-Hinkley"""


class PageHinkley:
    def __init__(self, delta=0.005, lamda=50):
        self.x_mean = 0
        self.sum = 0
        self.sum_min = 0
        self.num = 0
        self._delta = delta
        self._lambda = lamda
        self.change_detected = False

    def reset_params(self):
        self.num = 0
        self.x_mean = 0
        self.sum = 0

    def set_input(self, x):
        """
        :param x: input data
        :return: boolean
        """
        self.detect_drift(x)
        return self.change_detected

    def detect_drift(self, x):
        # calculate the average and sum
        self.num += 1
        self.x_mean = (x + self.x_mean * (self.num - 1)) / self.num
        self.sum += x - self.x_mean - self._delta

        # compare the current sum with the mininum sum up to now
        self.sum_min = min(self.sum, self.sum_min)

        self.change_detected = True if self.sum - self.sum_min > self._lambda else False
        if self.change_detected:
            self.reset_params()
