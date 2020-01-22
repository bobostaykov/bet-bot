class Statistics:
    def __init__(self):
        self.matches_total   = 0
        self.matches_1       = 0
        self.matches_x       = 0
        self.matches_2       = 0
        self.streak_1        = 0
        self.streak_x        = 0
        self.streak_2        = 0
        self.max_streak_1    = 0
        self.max_streak_x    = 0
        self.max_streak_2    = 0
        self.min_coef_x1     = float('inf')
        self.min_coef_x2     = float('inf')
        self.max_coef_x1     = 0
        self.max_coef_x2     = 0
        self.sum_coef_x1     = 0
        self.sum_coef_x2     = 0
        self.last            = ''

    def get_average_coef_x1(self):
        return self.sum_coef_x1 / self.matches_total

    def get_average_coef_x2(self):
        return self.sum_coef_x2 / self.matches_total